from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .broker import Broker
    from .asset_type import AssetType

class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    asset_types: Mapped[list[AssetType]] = relationship(
        back_populates="country"
    )

    brokers: Mapped[list[Broker]] = relationship(
        back_populates="country"
    )
