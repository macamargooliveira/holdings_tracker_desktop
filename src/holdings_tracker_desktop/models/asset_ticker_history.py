from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .base import Base

if TYPE_CHECKING:
    from .asset import Asset

class AssetTickerHistory(Base):
    __tablename__ = "asset_ticker_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    old_ticker: Mapped[str] = mapped_column(String(5), nullable=False)
    new_ticker: Mapped[str] = mapped_column(String(5), nullable=False)

    change_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    asset: Mapped[Asset] = relationship(back_populates="ticker_history")
