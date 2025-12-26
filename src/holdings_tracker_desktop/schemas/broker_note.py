from datetime import date as Date
from decimal import Decimal
from typing import Optional
from pydantic import Field, field_validator, model_validator
from .base import BaseSchema, TimestampSchema
from holdings_tracker_desktop.models.broker_note import OperationType

class BrokerNoteBase(BaseSchema):
    date: Date
    operation: OperationType
    broker_id: int = Field(..., gt=0)
    asset_id: int = Field(..., gt=0)

    quantity: Decimal = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)

    fees: Decimal = Field(default=Decimal("0"))
    taxes: Decimal = Field(default=Decimal("0"))

    note_number: Optional[str] = Field(
        None,
        max_length=30
    )

    @field_validator("fees", "taxes", mode="before")
    @classmethod
    def non_negative_decimals(cls, v: Decimal) -> Decimal:
        if v is None:
            return Decimal("0")
        if v < 0:
            raise ValueError("Value cannot be negative")
        return v

class BrokerNoteCreate(BrokerNoteBase):
    model_config = {
        "extra": "forbid"
    }

class BrokerNoteUpdate(BaseSchema):
    date: Optional[Date] = None
    operation: Optional[OperationType] = None
    broker_id: Optional[int] = Field(None, gt=0)

    quantity: Optional[Decimal] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, gt=0)

    fees: Optional[Decimal] = Field(None, ge=0)
    taxes: Optional[Decimal] = Field(None, ge=0)

    note_number: Optional[str] = Field(
        None,
        max_length=30
    )

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if not self.model_fields_set:
            raise ValueError(
                "At least one field must be provided for update"
            )
        return self

    model_config = {
        "extra": "forbid"
    }

class BrokerNoteResponse(BrokerNoteBase, TimestampSchema):
    id: int
    total_value: Decimal

    model_config = {
        "from_attributes": True
    }
