from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Enum, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from decimal import Decimal
from .base import BaseModel

if TYPE_CHECKING:
    from .asset import Asset
    from .broker import Broker

class OperationType(PyEnum):
    BUY = "BUY"
    SELL = "SELL"

class BrokerNote(BaseModel):
    __tablename__ = "broker_notes"

    date: Mapped[Date] = mapped_column(
        Date, 
        nullable=False
    )

    operation: Mapped[OperationType] = mapped_column(
        Enum(OperationType), 
        nullable=False
    )

    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id"), 
        nullable=False
    )

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"), 
        nullable=False
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(20, 6), 
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(20, 6), 
        nullable=False
    )

    fees: Mapped[Decimal] = mapped_column(
        Numeric(20, 6), 
        default=0
    )

    taxes: Mapped[Decimal] = mapped_column(
        Numeric(20, 6), 
        default=0
    )

    note_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    broker: Mapped[Broker] = relationship(
        back_populates="broker_notes"
    )

    asset: Mapped[Asset] = relationship(
        back_populates="broker_notes"
    )

    @property
    def total_value(self):
        return (self.quantity * self.price) + self.fees + self.taxes
