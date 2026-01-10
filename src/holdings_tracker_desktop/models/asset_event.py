from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from enum import Enum as PyEnum
from decimal import Decimal
from .base import AuditableModel

if TYPE_CHECKING:
    from .asset import Asset

class AssetEventType(PyEnum):
    # Corporate Actions
    SPLIT = "SPLIT"
    REVERSE_SPLIT = "REVERSE_SPLIT"

    # Financial Events
    AMORTIZATION = "AMORTIZATION"
    SUBSCRIPTION = "SUBSCRIPTION"

    # Conversion Event
    CONVERSION = "CONVERSION"

class AssetEvent(AuditableModel):
    __tablename__ = "asset_events"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"), 
        nullable=False
    )

    event_type: Mapped[AssetEventType] = mapped_column(
        Enum(AssetEventType), 
        nullable=False
    )

    date: Mapped[Date] = mapped_column(
        Date, 
        nullable=False
    )

    # Used only for SPLIT/REVERSE_SPLIT.
    factor: Mapped[Decimal | None] = mapped_column(Numeric(10, 6), nullable=True)

    # Used only for AMORTIZATION/SUBSCRIPTION.
    quantity: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    price: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)

    # Used only for CONVERSION.
    converted_to_asset_id: Mapped[int | None] = mapped_column(ForeignKey("assets.id"), nullable=True)
    conversion_quantity: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    residual_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)

    asset: Mapped[Asset] = relationship(
        back_populates="events",
        foreign_keys=[asset_id],
        cascade="save-update",
        lazy="selectin"
    )

    @validates("event_type")
    def _validate_event_type(self, key, value):
        if self.id is not None and value != self.event_type:
            raise ValueError("Type cannot be changed")
        return value

    def to_response(self) -> dict:
        """Convert to dictionary compatible with AssetEventResponse"""
        from holdings_tracker_desktop.schemas.asset_event import AssetEventResponse
        return AssetEventResponse.model_validate(self).model_dump()

    @classmethod
    def from_create_schema(cls, schema_data: dict) -> Asset:
        """Create instance from creation schema"""
        from holdings_tracker_desktop.schemas.asset_event import AssetEventCreate

        validated_data = AssetEventCreate(**schema_data).model_dump()
        return cls(**validated_data)

    def update_from_schema(self, schema_data: dict):
        """Update instance from update schema"""
        from holdings_tracker_desktop.schemas.asset_event import AssetEventUpdate

        update_data = AssetEventUpdate(**schema_data).model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(self, key, value)

    def to_ui_dict(self) -> dict:
        """Optimized for PySide6 table widgets"""
        return {
            'id': self.id,
            'asset_ticker': self.asset.ticker if self.asset else '',
            'event_type': self.event_type,
            'date': self.date,
            'factor': self.factor,
            'quantity': self.quantity,
            'price': self.price,
            'converted_to_asset_id': self.converted_to_asset_id,
            'conversion_quantity': self.conversion_quantity,
            'residual_value': self.residual_value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<AssetEventType(id={self.id}, asset_id={self.asset_id}, event_type={self.event_type})>"
