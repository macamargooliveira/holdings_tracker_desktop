from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import AuditableModel

class AppMetadata(AuditableModel):
    __tablename__ = "app_metadata"

    key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    value: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
