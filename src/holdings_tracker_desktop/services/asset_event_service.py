from typing import List
from sqlalchemy.orm import Session
from holdings_tracker_desktop.models.asset_event import AssetEvent
from holdings_tracker_desktop.schemas.asset_event import (
  AssetEventCreate, AssetEventUpdate, AssetEventResponse
)
from holdings_tracker_desktop.repositories.base_repository import BaseRepository
from holdings_tracker_desktop.services.position_snapshot_service import PositionSnapshotService

class AssetEventService:
    def __init__(self, db: Session):
        self.repository = BaseRepository[AssetEvent, AssetEventCreate, AssetEventUpdate](
            model=AssetEvent,
            db=db
        )
        self.position_snapshot_service = PositionSnapshotService(db)

    def create(self, data: AssetEventCreate) -> AssetEventResponse:
        """Create new AssetEvent with validation"""
        asset_event = self.repository.create_from_schema(data)

        self.position_snapshot_service.rebuild_from(
            asset_id=asset_event.asset_id,
            from_date=asset_event.date
        )

        return AssetEventResponse.model_validate(asset_event)

    def get(self, asset_event_id: int) -> AssetEventResponse:
        """Get AssetEvent by ID"""
        asset_event = self.repository.get_or_raise(asset_event_id)
        return AssetEventResponse.model_validate(asset_event)

    def update(self, asset_event_id: int, data: AssetEventUpdate) -> AssetEventResponse:
        """Update AssetEvent"""
        existing = self.repository.get_or_raise(asset_event_id)

        old_date = existing.date
        asset_id = existing.asset_id

        updated = self.repository.update_from_schema(asset_event_id, data)

        rebuild_from_date = min(old_date, updated.date)

        self.position_snapshot_service.rebuild_from(
            asset_id=asset_id,
            from_date=rebuild_from_date
        )

        return AssetEventResponse.model_validate(updated)

    def delete(self, asset_event_id: int) -> bool:
        """Delete AssetEvent"""
        asset_event = self.repository.get_or_raise(asset_event_id)

        asset_id = asset_event.asset_id
        from_date = asset_event.date

        deleted = self.repository.delete(asset_event_id)

        if deleted:
            self.position_snapshot_service.rebuild_from(
                asset_id=asset_id,
                from_date=from_date
            )

        return deleted

    def list_all_for_ui(
        self,
        asset_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[dict]:
        """Get AssetEvents already formatted for UI"""
        asset_events = sorted(
            self.repository.find_all_by(asset_id=asset_id, skip=skip, limit=limit),
            key=lambda s: s.date,
            reverse=True
        )
        return [ae.to_ui_dict() for ae in asset_events]

    def count_all(self) -> int:
        """Count all AssetEvents"""
        return self.repository.count()
