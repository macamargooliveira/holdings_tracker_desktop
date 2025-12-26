from datetime import datetime as DateTime
from typing import List
from sqlalchemy.orm import Session
from holdings_tracker_desktop.models.position_snapshot import PositionSnapshot
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

    def create(self, data: PositionSnapshotCreate) -> PositionSnapshotResponse:
        """Create new PositionSnapshot with validation"""
        position_snapshot = self.repository.create_from_schema(data)
        return PositionSnapshotResponse.model_validate(position_snapshot)

    def get(self, position_snapshot_id: int) -> PositionSnapshotResponse:
        """Get PositionSnapshot by ID"""
        position_snapshot = self.repository.get_or_raise(position_snapshot_id)
        return PositionSnapshotResponse.model_validate(position_snapshot)

    def update(self, position_snapshot_id: int, data: PositionSnapshotUpdate) -> PositionSnapshotResponse:
        """Update PositionSnapshot"""
        updated = self.repository.update_from_schema(position_snapshot_id, data)
        return PositionSnapshotResponse.model_validate(updated)

    def delete(self, position_snapshot_id: int) -> bool:
        """Delete PositionSnapshot"""
        return self.repository.delete(position_snapshot_id)

    def list_all(
        self,
        skip: int = 0, 
        limit: int = 100,
        order_by: DateTime = "created_at",
        descending: bool = True
    ) -> List[PositionSnapshotResponse]:
        """List all PositionSnapshots"""
        position_snapshots = self.repository.get_all(skip, limit, order_by, descending)
        return [PositionSnapshotResponse.model_validate(ps) for ps in position_snapshots]

    def list_all_models(self, order_by: DateTime = "created_at") -> List[PositionSnapshot]:
        """Get all PositionSnapshots as SQLAlchemy models"""
        return self.repository.get_all(order_by=order_by)

    def list_all_for_ui(
        self, 
        skip: int = 0, 
        limit: int = 100,
        order_by: DateTime = "created_at",
        descending: bool = True
    ) -> List[dict]:
        """Get PositionSnapshots already formatted for UI"""
        position_snapshots = self.repository.get_all(skip, limit, order_by, descending)
        return [ps.to_ui_dict() for ps in position_snapshots]

    def count_all(self) -> int:
        """Count all PositionSnapshots"""
        return self.repository.count()
