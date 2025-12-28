from datetime import date as Date
from decimal import Decimal
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from holdings_tracker_desktop.models.asset import Asset
from holdings_tracker_desktop.models.position_snapshot import PositionSnapshot
from holdings_tracker_desktop.models.broker_note import BrokerNote, OperationType
from holdings_tracker_desktop.schemas.position_snapshot import (
  PositionSnapshotCreate, PositionSnapshotUpdate, PositionSnapshotResponse
)
from holdings_tracker_desktop.repositories.base import BaseRepository

class PositionSnapshotService:
    def __init__(self, db: Session):
        self.repository = BaseRepository[PositionSnapshot, PositionSnapshotCreate, PositionSnapshotUpdate](
            model=PositionSnapshot,
            db=db
        )
        self.db = db

    def create(self, data: PositionSnapshotCreate) -> PositionSnapshotResponse:
        """Create new PositionSnapshot with validation"""
        position_snapshot = self.repository.create_from_schema(data)
        return PositionSnapshotResponse.model_validate(position_snapshot)

    def get(self, position_snapshot_id: int) -> PositionSnapshotResponse:
        """Get PositionSnapshot by ID"""
        position_snapshot = self.repository.get_or_raise(position_snapshot_id)
        return PositionSnapshotResponse.model_validate(position_snapshot)

    def list_all(
        self,
        skip: int = 0, 
        limit: int = 100,
        order_by: Date = "snapshot_date",
        descending: bool = True
    ) -> List[PositionSnapshotResponse]:
        """List all PositionSnapshots"""
        position_snapshots = self.repository.get_all(skip, limit, order_by, descending)
        return [PositionSnapshotResponse.model_validate(ps) for ps in position_snapshots]

    def list_all_models(self, order_by: Date = "snapshot_date") -> List[PositionSnapshot]:
        """Get all PositionSnapshots as SQLAlchemy models"""
        return self.repository.get_all(order_by=order_by)

    def list_all_for_ui(
        self, 
        asset_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[dict]:
        """Get PositionSnapshots already formatted for UI"""
        snapshots = sorted(
            self.repository.find_all_by(asset_id=asset_id, skip=skip, limit=limit),
            key=lambda s: s.snapshot_date,
            reverse=True
        )
        return [s.to_ui_dict() for s in snapshots]

    def count_all(self) -> int:
        """Count all PositionSnapshots"""
        return self.repository.count()

    def get_earliest_snapshot_date(self) -> Date | None:
        min_date: Date | None = self.db.query(func.min(PositionSnapshot.snapshot_date)).scalar()
        return min_date

    def get_allocation_by_asset(self, year: int, asset_type_id: int | None = None) -> list[dict]:
        subquery = (
            self.db.query(
                PositionSnapshot.asset_id,
                func.max(PositionSnapshot.snapshot_date).label("max_date")
            )
            .filter(func.extract("year", PositionSnapshot.snapshot_date) == year)
            .group_by(PositionSnapshot.asset_id)
            .subquery()
        )

        total_cost = func.sum(PositionSnapshot.quantity * PositionSnapshot.avg_price).label("total_cost")

        query = (
            self.db.query(Asset.ticker, total_cost)
            .join(PositionSnapshot, PositionSnapshot.asset_id == Asset.id)
            .join(
                subquery,
                (PositionSnapshot.asset_id == subquery.c.asset_id) &
                (PositionSnapshot.snapshot_date == subquery.c.max_date)
            )
        )

        if asset_type_id is not None:
            query = query.filter(Asset.type_id == asset_type_id)

        rows = (
            query
            .group_by(Asset.ticker)
            .order_by(total_cost.desc())
            .all()
        )

        return [
            {"label": ticker, "value": float(total)}
            for ticker, total in rows
            if total > 0
        ]

    def rebuild_from(self, asset_id: int, from_date: Date) -> None:
        """
        Rebuild incremental snapshots for an asset starting from a given date.
        All snapshots >= from_date are deleted and rebuilt.
        """
        try:
            self._delete_snapshots_from(asset_id, from_date)
            qty, cost = self._load_state_before(asset_id, from_date)
            self._build_from_notes(asset_id, from_date, qty, cost)
            self.repository.save_changes()
        except Exception:
            self.repository.rollback()
            raise

    def _delete_snapshots_from(self, asset_id: int, from_date: Date) -> None:
        self.db.query(PositionSnapshot).filter(
            PositionSnapshot.asset_id == asset_id,
            PositionSnapshot.snapshot_date >= from_date
        ).delete(synchronize_session=False)

    def _load_state_before(self, asset_id: int, from_date: Date) -> tuple[Decimal, Decimal]:
        snapshot = (
            self.db.query(PositionSnapshot)
            .filter(
                PositionSnapshot.asset_id == asset_id,
                PositionSnapshot.snapshot_date < from_date
            )
            .order_by(PositionSnapshot.snapshot_date.desc())
            .first()
        )

        if not snapshot:
            return Decimal("0"), Decimal("0")

        quantity = snapshot.quantity
        total_cost = snapshot.total_cost

        return quantity, total_cost

    def _build_from_notes(self, asset_id: int, from_date: Date, quantity: Decimal, total_cost: Decimal) -> None:
        notes = self._load_notes(asset_id, from_date)

        last_date: Date | None = None

        for note in notes:
            if last_date and note.date != last_date:
                self._add_snapshot(asset_id, last_date, quantity, total_cost)

            quantity, total_cost = self._apply_note(note, quantity, total_cost)
            last_date = note.date

        if last_date:
            self._add_snapshot(asset_id, last_date, quantity, total_cost)

    def _load_notes(self, asset_id: int, from_date: Date) -> list[BrokerNote]:
        return (
            self.db.query(BrokerNote)
            .filter(
                BrokerNote.asset_id == asset_id,
                BrokerNote.date >= from_date
            )
            .order_by(BrokerNote.date)
            .all()
        )

    def _apply_note(self, note: BrokerNote, quantity: Decimal, total_cost: Decimal) -> tuple[Decimal, Decimal]:
        if note.operation == OperationType.BUY:
            return (
                quantity + note.quantity,
                total_cost + note.total_value
            )

        if note.operation == OperationType.SELL and quantity > 0:
            avg_price = total_cost / quantity
            new_quantity = quantity - note.quantity
            new_cost = total_cost - (avg_price * note.quantity)

            if new_quantity <= 0:
                return Decimal("0"), Decimal("0")

            return new_quantity, new_cost

        return quantity, total_cost

    def _add_snapshot(self, asset_id: int, snapshot_date: Date, quantity: Decimal, total_cost: Decimal) -> None:
        avg_price = (
            total_cost / quantity
            if quantity > 0
            else Decimal("0")
        )

        self.db.add(
            PositionSnapshot(
                asset_id=asset_id,
                snapshot_date=snapshot_date,
                quantity=quantity,
                avg_price=avg_price
            )
        )
