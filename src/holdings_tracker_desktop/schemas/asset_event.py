from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import Field, model_validator
from .base import BaseSchema, AuditableSchema
from ..models.asset_event import AssetEventType

REQUIRED_FIELDS_BY_EVENT_TYPE: dict[str, set[str]] = {
    "SPLIT": {"factor"},
    "REVERSE_SPLIT": {"factor"},

    "AMORTIZATION": {"quantity", "price"},
    "SUBSCRIPTION": {"quantity", "price"},

    "CONVERSION": {
        "converted_to_asset_id",
        "conversion_quantity",
    }
}

class AssetEventBase(BaseSchema):
    asset_id: int = Field(..., gt=0)
    event_type: AssetEventType
    date: date

    factor: Optional[Decimal] = Field(None, gt=0)

    quantity: Optional[Decimal] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, gt=0)

    converted_to_asset_id: Optional[int] = Field(None, gt=0)
    conversion_quantity: Optional[Decimal] = Field(None, gt=0)
    residual_value: Optional[Decimal] = Field(None, ge=0)

class AssetEventCreate(AssetEventBase):

    @model_validator(mode="after")
    def validate_required_fields_by_event_type(self):
        required_fields = REQUIRED_FIELDS_BY_EVENT_TYPE.get(
            self.event_type.value, set()
        )

        missing_fields = [
            field
            for field in required_fields
            if getattr(self, field) is None
        ]

        if missing_fields:
            raise ValueError(
                f"Missing required fields for event_type={self.event_type.value}: "
                f"{', '.join(missing_fields)}"
            )
        
        return self

    model_config = {
        "extra": "forbid"
    }

class AssetEventUpdate(AssetEventBase):

  @model_validator(mode="after")
  def validate_required_fields_by_event_type(self):
      required_fields = REQUIRED_FIELDS_BY_EVENT_TYPE.get(
          self.event_type.value, set()
      )

      missing_fields = [
          field
          for field in required_fields
          if getattr(self, field) is None
      ]

      if missing_fields:
          raise ValueError(
              f"Missing required fields for event_type={self.event_type.value}: "
              f"{', '.join(missing_fields)}"
          )
      
      return self

  model_config = {
      "extra": "forbid"
  }

class AssetEventResponse(AssetEventBase, AuditableSchema):
    model_config = {
        "from_attributes": True
    }
