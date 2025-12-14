from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from decimal import Decimal
from .base import BaseModel

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

class AssetEvent(BaseModel):
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
        foreign_keys=[asset_id]
    )
