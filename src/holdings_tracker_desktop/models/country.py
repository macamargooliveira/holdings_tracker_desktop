from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import AuditableModel

if TYPE_CHECKING:
    from .broker import Broker
    from .asset_type import AssetType

class Country(AuditableModel):
    __tablename__ = "countries"

    name: Mapped[str] = mapped_column(
        String(80), 
        unique=True, 
        nullable=False
    )

    asset_types: Mapped[list[AssetType]] = relationship(
        back_populates="country",
        cascade="save-update",
        lazy="selectin"
    )

    brokers: Mapped[list[Broker]] = relationship(
        back_populates="country",
        cascade="save-update",
        lazy="selectin"
    )

    def to_response(self) -> dict:
        """Convert to dictionary compatible with CountryResponse"""
        from holdings_tracker_desktop.schemas.country import CountryResponse
        return CountryResponse.model_validate(self).model_dump()

    @classmethod
    def from_create_schema(cls, schema_data: dict) -> Country:
        """Create instance from creation schema"""
        from holdings_tracker_desktop.schemas.country import CountryCreate

        validated_data = CountryCreate(**schema_data).model_dump()
        return cls(**validated_data)

    def update_from_schema(self, schema_data: dict):
        """Update instance from update schema"""
        from holdings_tracker_desktop.schemas.country import CountryUpdate

        update_data = CountryUpdate(**schema_data).model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(self, key, value)

    @property
    def asset_types_count(self) -> int:
        return len(self.asset_types)

    @property
    def brokers_count(self) -> int:
        return len(self.brokers)

    def validate_for_deletion(self) -> tuple[bool, str]:
        """
        Validate if country can be deleted.
        
        Returns:
            Tuple of (can_delete: bool, reason: str)
        """
        if self.brokers_count > 0:
            return (
                False, 
                f"Cannot delete '{self.name}' because it has {self.brokers_count} associated brokers"
            )

        if self.asset_types_count > 0:
            return (
                False, 
                f"Cannot delete '{self.name}' because it has {self.asset_types_count} associated asset types"
            )

        return True, ""

    def to_ui_dict(self) -> dict:
        """Optimized for PySide6 table widgets"""
        return {
            'id': self.id,
            'name': self.name,
            'asset_types_count': self.asset_types_count,
            'brokers_count': self.brokers_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<Country(id={self.id}, name={self.name})>"
