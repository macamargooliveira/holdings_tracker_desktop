from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from .base import BaseModel

if TYPE_CHECKING:
    from .asset import Asset

class AssetEventType(PyEnum):
    AMORTIZATION = "AMORTIZATION"
    REVERSE_SPLIT = "REVERSE_SPLIT"
    SPLIT = "SPLIT"
    SUBSCRIPTION = "SUBSCRIPTION"

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

    # Used only for AMORTIZATION and SUBSCRIPTION.
    quantity: Mapped[float | None] = mapped_column(
        Numeric(20, 6), 
        nullable=True
    )

    # Used only for AMORTIZATION and SUBSCRIPTION.
    price: Mapped[float | None] = mapped_column(
        Numeric(20, 6), 
        nullable=True
    )

    # Used only for SPLIT and REVERSE_SPLIT.
    factor: Mapped[float | None] = mapped_column(
        Numeric(10, 6), 
        nullable=True
    )

    asset: Mapped[Asset] = relationship(
        back_populates="events"
    )
