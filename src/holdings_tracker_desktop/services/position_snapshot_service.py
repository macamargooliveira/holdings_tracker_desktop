from datetime import date as Date
from decimal import Decimal
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from holdings_tracker_desktop.models import Asset, AssetEvent, BrokerNote, PositionSnapshot
from holdings_tracker_desktop.models.asset_event import AssetEventType
from holdings_tracker_desktop.models.broker_note import OperationType
from holdings_tracker_desktop.schemas.position_snapshot import (
  PositionSnapshotCreate, PositionSnapshotUpdate, PositionSnapshotResponse
)
from holdings_tracker_desktop.repositories.base_repository import BaseRepository

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

    def list_all_for_ui(
        self, 
        asset_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[dict]:
        """Get PositionSnapshots already formatted for UI"""
        snapshots = sorted(
            self.repository.find_all_by(asset_id=asset_id, skip=skip, limit=limit),
            key=lambda s: (s.snapshot_date, s.id),
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
            .filter(func.extract("year", PositionSnapshot.snapshot_date) <= year)
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
            timeline = self._load_timeline(asset_id, from_date)
            self._build_from_timeline(asset_id, timeline, qty, cost)
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

        return snapshot.quantity, snapshot.total_cost

    def _load_timeline(self, asset_id: int, from_date: Date) -> list:
        notes = (
            self.db.query(BrokerNote)
            .filter(
                BrokerNote.asset_id == asset_id,
                BrokerNote.date >= from_date,
            )
            .all()
        )

        events = (
            self.db.query(AssetEvent)
            .filter(
                AssetEvent.asset_id == asset_id,
                AssetEvent.date >= from_date,
            )
            .all()
        )

        timeline = notes + events

        # AssetEvent takes precedence over BrokerNote
        timeline.sort(
            key=lambda x: (
                x.date,
                0 if isinstance(x, AssetEvent) else 1
            )
        )

        return timeline

    def _build_from_timeline(self, asset_id: int, timeline: list, quantity: Decimal, total_cost: Decimal) -> None:
        for item in timeline:
            if isinstance(item, AssetEvent):
                quantity, total_cost = self._apply_asset_event(item, quantity, total_cost)

            elif isinstance(item, BrokerNote):
                quantity, total_cost = self._apply_broker_note(item, quantity, total_cost)

            self._add_snapshot(asset_id, item.date, quantity, total_cost)

    def _apply_asset_event(self, event: AssetEvent, quantity: Decimal, total_cost: Decimal) -> tuple[Decimal, Decimal]:
        if quantity <= 0:
            return quantity, total_cost

        match event.event_type:
            case AssetEventType.SPLIT | AssetEventType.REVERSE_SPLIT:
                if not event.factor or event.factor <= 0:
                    return quantity, total_cost

                new_quantity = quantity / event.factor

                if new_quantity <= 0:
                    return Decimal("0"), Decimal("0")

                return new_quantity, total_cost

            case AssetEventType.AMORTIZATION:
                event_quantity = event.quantity or quantity
                event_price = event.price or Decimal("0")

                amortized_value = event_quantity * event_price
                new_total_cost = total_cost - amortized_value

                if new_total_cost <= 0:
                    return quantity, Decimal("0")

                return quantity, new_total_cost

            case AssetEventType.SUBSCRIPTION:
                event_quantity = event.quantity or Decimal("0")
                event_price = event.price or Decimal("0")

                added_cost = event_quantity * event_price

                return (
                    quantity + event_quantity,
                    total_cost + added_cost,
                )

            case _:
                return quantity, total_cost

    def _apply_broker_note(self, note: BrokerNote, quantity: Decimal, total_cost: Decimal) -> tuple[Decimal, Decimal]:
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
        avg_price = total_cost / quantity if quantity > 0 else Decimal("0")

        self.db.add(
            PositionSnapshot(
                asset_id=asset_id,
                snapshot_date=snapshot_date,
                quantity=quantity,
                avg_price=avg_price
            )
        )
