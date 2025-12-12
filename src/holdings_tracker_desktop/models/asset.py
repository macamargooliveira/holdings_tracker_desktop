from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel

if TYPE_CHECKING:
    from .asset_event import AssetEvent
    from .asset_sector import AssetSector
    from .asset_type import AssetType
    from .broker_note import BrokerNote
    from .currency import Currency
    from .position_snapshot import PositionSnapshot
    from .asset_ticker_history import AssetTickerHistory

class Asset(BaseModel):
    __tablename__ = "assets"

    ticker: Mapped[str] = mapped_column(
        String(5), 
        unique=True, 
        nullable=False
    )

    type_id: Mapped[int] = mapped_column(
        ForeignKey("asset_types.id"), 
        nullable=False
    )

    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"), 
        nullable=False
    )

    sector_id: Mapped[int | None] = mapped_column(
        ForeignKey("asset_sectors.id"), 
        nullable=True
    )

    asset_type: Mapped[AssetType] = relationship(
        back_populates="assets"
    )

    currency: Mapped[Currency] = relationship(
        back_populates="assets"
    )

    sector: Mapped[AssetSector] = relationship(
        back_populates="assets"
    )

    broker_notes: Mapped[list[BrokerNote]] = relationship(
        back_populates="asset"
    )

    snapshots: Mapped[list[PositionSnapshot]] = relationship(
        back_populates="asset"
    )

    events: Mapped[list[AssetEvent]] = relationship(
        back_populates="asset"
    )

    ticker_history: Mapped[list[AssetTickerHistory]] = relationship(
        back_populates="asset"
    )
