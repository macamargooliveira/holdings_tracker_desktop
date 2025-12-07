from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .asset import Asset
    from .asset_type import AssetType

class AssetSector(Base):
    __tablename__ = "asset_sectors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"), nullable=False)

    asset_type: Mapped[AssetType] = relationship(back_populates="sectors")

    assets: Mapped[list[Asset]] = relationship(
        back_populates="sector"
    )
