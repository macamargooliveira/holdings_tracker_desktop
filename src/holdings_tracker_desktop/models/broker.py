from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel

if TYPE_CHECKING:
    from .broker_note import BrokerNote
    from .country import Country

class Broker(BaseModel):
    __tablename__ = "brokers"

    name: Mapped[str] = mapped_column(
        String(80), 
        unique=True, 
        nullable=False
    )

    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"), 
        nullable=False
    )

    country: Mapped[Country] = relationship(
        back_populates="brokers"
    )

    broker_notes: Mapped[list[BrokerNote]] = relationship(
        back_populates="broker"
    )
