from pydantic import Field, model_validator
from typing import Optional
from .base import BaseSchema, TimestampSchema

class AssetTypeBase(BaseSchema):
    name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="Asset type name (e.g., 'Stock', 'FII', 'Bond')"
    )
    country_id: int = Field(
        ...,
        gt=0,
        description="ID of the country where this asset type is valid"
    )

class AssetTypeCreate(AssetTypeBase):
    @model_validator(mode='after')
    def validate_name_format(self):
        self.name = self.name.strip()
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ação",
                "country_id": 1
            }
        }
    }

class AssetTypeUpdate(BaseSchema):
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=20
    )
    country_id: Optional[int] = Field(
        None,
        gt=0
    )

    @model_validator(mode='after')
    def validate_at_least_one_field(self):
        if all(v is None for v in [self.name, self.country_id]):
            raise ValueError("At least one field must be provided for update")
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "FII",
                "country_id": 1
            }
        }
    }

class AssetTypeResponse(AssetTypeBase, TimestampSchema):
    id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Ação",
                "country_id": 1,
                "created_at": "2025-01-01T10:00:00",
                "updated_at": "2025-01-01T10:00:00"
            }
        }
    }

class AssetTypeFilters(BaseSchema):
    name: Optional[str] = Field(
        None, 
        description="Filter by name (case-insensitive)"
    )
    country_id: Optional[int] = Field(
        None, 
        gt=0,
        description="Filter by country ID"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ação",
                "country_id": 1
            }
        }
    }
