from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import AuditableModel

if TYPE_CHECKING:
    from .asset import Asset

class AssetTickerHistory(AuditableModel):
    __tablename__ = "asset_ticker_histories"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"), 
        nullable=False
    )

    old_ticker: Mapped[str] = mapped_column(
        String(12), 
        nullable=False
    )

    new_ticker: Mapped[str] = mapped_column(
        String(12), 
        nullable=False
    )

    change_date: Mapped[Date] = mapped_column(
        Date, 
        nullable=False
    )

    asset: Mapped[Asset] = relationship(
        back_populates="ticker_histories",
        cascade="save-update",
        lazy="selectin"
    )

    def to_response(self) -> dict:
        """Convert to dictionary compatible with AssetTickerHistoryResponse"""
        from holdings_tracker_desktop.schemas.asset_ticker_history import AssetTickerHistoryResponse
        return AssetTickerHistoryResponse.model_validate(self).model_dump()

    def to_ui_dict(self) -> dict:
        """Optimized for PySide6 table widgets"""
        return {
            'id': self.id,
            'change_date': self.change_date,
            'asset_ticker': self.asset.ticker if self.asset else '',
            'old_ticker': self.old_ticker,
            'new_ticker': self.new_ticker,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<AssetTickerHistory(id={self.id}, change_date={self.date}, asset_id={self.asset_id})>"
