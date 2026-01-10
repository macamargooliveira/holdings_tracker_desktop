from datetime import date as Date
from decimal import Decimal
from pydantic import Field
from .base import BaseSchema, IdentifiedSchema

class PositionSnapshotBase(BaseSchema):
    asset_id: int = Field(..., gt=0)
    snapshot_date: Date
    quantity: Decimal = Field(..., gt=0)
    avg_price: Decimal = Field(..., gt=0)

class PositionSnapshotCreate(PositionSnapshotBase):
    model_config = {
        "extra": "forbid"
    }

class PositionSnapshotUpdate(PositionSnapshotBase):
    pass

class PositionSnapshotResponse(PositionSnapshotBase, IdentifiedSchema):
    total_cost: Decimal

    model_config = {
        "from_attributes": True
    }
