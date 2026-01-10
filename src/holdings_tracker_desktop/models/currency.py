from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import AuditableModel

if TYPE_CHECKING:
    from .asset import Asset

class Currency(AuditableModel):
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
        back_populates="currency",
        cascade="save-update",
        lazy="dynamic"
    )

    def to_response(self) -> dict:
        """Convert to dictionary compatible with CurrencyResponse"""
        from holdings_tracker_desktop.schemas.currency import CurrencyResponse
        return CurrencyResponse.model_validate(self).model_dump()

    @classmethod
    def from_create_schema(cls, schema_data: dict) -> Currency:
        """Create instance from creation schema"""
        from holdings_tracker_desktop.schemas.currency import CurrencyCreate

        validated_data = CurrencyCreate(**schema_data).model_dump()
        return cls(**validated_data)

    def update_from_schema(self, schema_data: dict):
        """Update instance from update schema"""
        from holdings_tracker_desktop.schemas.currency import CurrencyUpdate

        update_data = CurrencyUpdate(**schema_data).model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(self, key, value)

    @property
    def assets_count(self) -> int:
        return self.assets.count()

    def validate_for_deletion(self) -> tuple[bool, str]:
        """
        Validate if currency can be deleted.
        
        Returns:
            Tuple of (can_delete: bool, reason: str)
        """
        count = self.assets_count
        if count > 0:
            return (
                False, 
                f"Cannot delete '{self.code}' because it has {count} associated assets"
            )

        return True, ""

    def to_ui_dict(self) -> dict:
        """Optimized for PySide6 table widgets"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'symbol': self.symbol,
            'assets_count': self.assets_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<Currency(id={self.id}, code={self.code})>"
