from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .asset import Asset
    from .asset_sector import AssetSector
    from .country import Country

class AssetType(Base):
    __tablename__ = "asset_types"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), nullable=False)

    country: Mapped[Country] = relationship(back_populates="asset_types")

    assets: Mapped[list[Asset]] = relationship(
        back_populates="asset_type"
    )

    sectors: Mapped[list[AssetSector]] = relationship(
        back_populates="asset_type"
    )
