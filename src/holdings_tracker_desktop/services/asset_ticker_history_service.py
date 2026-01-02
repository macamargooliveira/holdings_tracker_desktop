from datetime import date as Date
from typing import List
from sqlalchemy.orm import Session
from holdings_tracker_desktop.models.asset_ticker_history import AssetTickerHistory
from holdings_tracker_desktop.schemas.asset_ticker_history import (
  AssetTickerHistoryCreate, AssetTickerHistoryUpdate, AssetTickerHistoryResponse
)
from holdings_tracker_desktop.repositories.base import BaseRepository

class AssetTickerHistoryService:
    def __init__(self, db: Session):
        self.repository = BaseRepository[AssetTickerHistory, AssetTickerHistoryCreate, AssetTickerHistoryUpdate](
            model=AssetTickerHistory,
            db=db
        )

    def create(self, data: AssetTickerHistoryCreate) -> AssetTickerHistoryResponse:
        """Change Asset ticker and register history"""
        from holdings_tracker_desktop.models.asset import Asset

        db = self.repository.db

        asset = (
            db.query(Asset)
            .filter(Asset.id == data.asset_id)
            .one_or_none()
        )

        if not asset:
            raise ValueError("Asset not found")

        if asset.ticker == data.new_ticker:
            raise ValueError("New ticker must be different from current ticker")

        history = AssetTickerHistory(
            asset=asset,
            old_ticker=asset.ticker,
            new_ticker=data.new_ticker,
            change_date=data.change_date,
        )

        asset.ticker = data.new_ticker

        db.add(history)
        db.flush()

        return AssetTickerHistoryResponse.model_validate(history)

    def get(self, asset_ticker_history_id: int) -> AssetTickerHistoryResponse:
        """Get AssetTickerHistory by ID"""
        asset_ticker_history = self.repository.get_or_raise(asset_ticker_history_id)
        return AssetTickerHistoryResponse.model_validate(asset_ticker_history)

    def delete(self, asset_id: int) -> bool:
        """Delete AssetTickerHistory"""
        return self.repository.delete(asset_id)

    def list_all(
        self, 
        skip: int = 0,
        limit: int = 100,
        order_by: Date = "change_date",
        descending: bool = True
    ) -> List[AssetTickerHistoryResponse]:
        """List all AssetTickerHistories"""
        asset_ticker_histories = self.repository.get_all(skip, limit, order_by, descending)
        return [AssetTickerHistoryResponse.model_validate(ath) for ath in asset_ticker_histories]

    def list_all_models(self, order_by: Date = "change_date") -> List[AssetTickerHistory]:
        """Get all AssetTickerHistories as SQLAlchemy models"""
        return self.repository.get_all(order_by=order_by)

    def list_all_for_ui(
        self,
        asset_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[dict]:
        """Get AssetTickerHistories already formatted for UI"""
        asset_ticker_histories = sorted(
            self.repository.find_all_by(asset_id=asset_id, skip=skip, limit=limit),
            key=lambda s: s.change_date,
            reverse=True
        )
        return [ath.to_ui_dict() for ath in asset_ticker_histories]

    def count_all(self) -> int:
        """Count all AssetTickerHistories"""
        return self.repository.count()
