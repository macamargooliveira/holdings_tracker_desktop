from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel

if TYPE_CHECKING:
    from .asset import Asset

class Currency(BaseModel):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(
        String(3), 
        unique=True, 
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(80), 
        nullable=False
    )

    symbol: Mapped[str] = mapped_column(
        String(3), 
        nullable=False
    )

    assets: Mapped[list[Asset]] = relationship(
        back_populates="currency"
    )
