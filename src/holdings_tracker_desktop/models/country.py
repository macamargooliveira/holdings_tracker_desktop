from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel

if TYPE_CHECKING:
    from .broker import Broker
    from .asset_type import AssetType

class Country(BaseModel):
    __tablename__ = "countries"

    name: Mapped[str] = mapped_column(
        String(80), 
        unique=True, 
        nullable=False
    )

    asset_types: Mapped[list[AssetType]] = relationship(
        back_populates="country"
    )

    brokers: Mapped[list[Broker]] = relationship(
        back_populates="country"
    )
