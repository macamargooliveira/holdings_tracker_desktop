from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import BaseModel

if TYPE_CHECKING:
    from .asset import Asset

class PositionSnapshot(BaseModel):
    __tablename__ = "position_snapshots"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"), 
        nullable=False
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(20, 6), 
        nullable=False
    )

    avg_price: Mapped[float] = mapped_column(
        Numeric(20, 6), 
        nullable=False
    )

    total_invested: Mapped[float] = mapped_column(
        Numeric(20, 6), 
        nullable=False
    )

    asset: Mapped[Asset] = relationship(
        back_populates="snapshots"
    )
