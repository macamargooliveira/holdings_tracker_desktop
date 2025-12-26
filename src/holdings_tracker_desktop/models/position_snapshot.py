from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from .base import BaseModel

if TYPE_CHECKING:
    from .asset import Asset

class PositionSnapshot(BaseModel):
    __tablename__ = "position_snapshots"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"), 
        nullable=False
    )

    snapshot_date: Mapped[Date] = mapped_column(
        Date, nullable=False
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(20, 6), 
        nullable=False
    )

    avg_price: Mapped[Decimal] = mapped_column(
        Numeric(20, 6), 
        nullable=False
    )

    asset: Mapped[Asset] = relationship(
        back_populates="snapshots",
        cascade="save-update",
        lazy="selectin"
    )

    def to_response(self) -> dict:
        """Convert to dictionary compatible with PositionSnapshotResponse"""
        from holdings_tracker_desktop.schemas.position_snapshot import PositionSnapshotResponse
        return PositionSnapshotResponse.model_validate(self).model_dump()

    @classmethod
    def from_create_schema(cls, schema_data: dict) -> PositionSnapshot:
        """Create instance from creation schema"""
        from holdings_tracker_desktop.schemas.position_snapshot import PositionSnapshotCreate

        validated_data = PositionSnapshotCreate(**schema_data).model_dump()
        return cls(**validated_data)

    def update_from_schema(self, schema_data: dict):
        """Update instance from update schema"""
        from holdings_tracker_desktop.schemas.position_snapshot import PositionSnapshotUpdate

        update_data = PositionSnapshotUpdate(**schema_data).model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(self, key, value)

    @property
    def total_cost(self):
        return self.quantity * self.avg_price

    def to_ui_dict(self) -> dict:
        """Optimized for PySide6 table widgets"""
        return {
            'id': self.id,
            'asset_ticker': self.asset.ticker if self.asset else '',
            'snapshot_date': self.snapshot_date,
            'asset_currency': self.asset.currency.symbol if self.asset else '',
            'quantity': self.quantity,
            'avg_price': self.avg_price,
            'total_cost': self.total_cost,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<PositionSnapshot(id={self.id}, asset_id={self.asset_id}, snapshot_date={self.snapshot_date})>"
