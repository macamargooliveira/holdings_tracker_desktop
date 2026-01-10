from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True
    )

class IdentifiedSchema(BaseSchema):
    id: int

class AuditableSchema(IdentifiedSchema):
    created_at: datetime
    updated_at: datetime
