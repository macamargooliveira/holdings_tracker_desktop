from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func, Integer

from holdings_tracker_desktop.utils.datetime import to_localtime

class Base(DeclarativeBase):
    """Base SQLAlchemy declarative class"""
    pass

class IdentifiedModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

class AuditableModel(IdentifiedModel):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    @hybrid_property
    def created_at_local(self) -> datetime:
        return to_localtime(self.created_at)
    
    @hybrid_property
    def updated_at_local(self) -> datetime:
        return to_localtime(self.updated_at)
