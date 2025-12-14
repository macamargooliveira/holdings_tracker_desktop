from pydantic import Field, model_validator
from typing import Optional
from .base import BaseSchema, TimestampSchema

class CountryBase(BaseSchema):
    name: str = Field(
        ...,
        min_length=2,
        max_length=80,
        description="Country name"
    )

class CountryCreate(CountryBase):
    @model_validator(mode='after')
    def validate_name_format(self):
        self.name = self.name.strip()
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Brasil"
            }
        }
    }

class CountryUpdate(BaseSchema):
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=80
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Brasil"
            }
        }
    }

class CountryResponse(CountryBase, TimestampSchema):
    id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Brasil",
                "created_at": "2025-01-01T10:00:00",
                "updated_at": "2025-01-01T10:00:00"
            }
        }
    }

class CountryFilters(BaseSchema):
    name: Optional[str] = Field(
        None, 
        description="Filter by name (case-insensitive)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Brasil"
            }
        }
    }
