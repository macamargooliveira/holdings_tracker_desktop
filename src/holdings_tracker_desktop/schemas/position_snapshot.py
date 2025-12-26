from datetime import datetime as DateTime
from decimal import Decimal
from typing import Optional
from pydantic import Field, model_validator
from .base import BaseSchema, TimestampSchema

class PositionSnapshotBase(BaseSchema):
    asset_id: int = Field(..., gt=0)
    timestamp: DateTime
    quantity: Decimal = Field(..., gt=0)
    avg_price: Decimal = Field(..., gt=0)

class PositionSnapshotCreate(PositionSnapshotBase):
    model_config = {
        "extra": "forbid"
    }

class PositionSnapshotUpdate(BaseSchema):
    asset_id: Optional[int] = Field(None, gt=0)
    timestamp: Optional[DateTime] = None
    quantity: Optional[Decimal] = Field(None, gt=0)
    avg_price: Optional[Decimal] = Field(None, gt=0)

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

class PositionSnapshotResponse(PositionSnapshotBase, TimestampSchema):
    id: int
    total_invested: Decimal

    model_config = {
        "from_attributes": True
    }
