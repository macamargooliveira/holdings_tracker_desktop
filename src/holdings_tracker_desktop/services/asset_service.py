from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from holdings_tracker_desktop.models.asset import Asset
from holdings_tracker_desktop.schemas.asset import (
  AssetCreate, AssetUpdate, AssetResponse
)
from holdings_tracker_desktop.repositories.base_repository import BaseRepository
from holdings_tracker_desktop.utils.exceptions import ConflictException

class AssetService:
    def __init__(self, db: Session):
        self.repository = BaseRepository[Asset, AssetCreate, AssetUpdate](
            model=Asset,
            db=db
        )

    def create(self, data: AssetCreate) -> AssetResponse:
        """Create new Asset with validation"""
        self._ensure_ticker_is_unique(data.ticker)

        asset = self.repository.create_from_schema(data)
        return AssetResponse.model_validate(asset)

    def get(self, asset_id: int) -> AssetResponse:
        """Get Asset by ID"""
        asset = self.repository.get_or_raise(asset_id)
        return AssetResponse.model_validate(asset)

    def update(self, asset_id: int, data: AssetUpdate) -> AssetResponse:
        """Update Asset"""
        updated = self.repository.update_from_schema(asset_id, data)
        return AssetResponse.model_validate(updated)

    def delete(self, asset_id: int) -> bool:
        """Delete Asset"""
        asset = self.repository.get_or_raise(asset_id)

        can_delete, error_message = asset.validate_for_deletion()
        if not can_delete:
            raise ConflictException(error_message)

        return self.repository.delete(asset_id)

    def list_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        order_by: str = "ticker",
        descending: bool = False
    ) -> List[AssetResponse]:
        """List all Assets"""
        assets = self.repository.get_all(skip, limit, order_by, descending)
        return [AssetResponse.model_validate(a) for a in assets]

    def list_all_models(self, order_by: str = "ticker") -> List[Asset]:
        """Get all Assets as SQLAlchemy models"""
        return self.repository.get_all(order_by=order_by)

    def list_all_for_ui(
        self, 
        skip: int = 0, 
        limit: int = 100,
        order_by: str = "ticker",
        descending: bool = False
    ) -> List[dict]:
        """Get Assets already formatted for UI"""
        assets = self.repository.get_all(skip, limit, order_by, descending)
        return [a.to_ui_dict() for a in assets]

    def count_all(self) -> int:
        """Count all Assets"""
        return self.repository.count()

    def _ensure_ticker_is_unique(
        self,
        ticker: str,
        exclude_id: int | None = None
    ) -> None:
        """
        Validate that Asset ticker is unique (case-insensitive).
        """
        query = (
            self.repository.db.query(Asset)
            .filter(func.lower(Asset.ticker) == ticker.lower())
        )

        if exclude_id is not None:
            query = query.filter(Asset.id != exclude_id)

        if self.repository.db.query(query.exists()).scalar():
            raise ConflictException(
                f"Asset '{ticker}' already exists"
            )
