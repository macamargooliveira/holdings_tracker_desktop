from typing import List, Optional
from sqlalchemy.orm import Session
from holdings_tracker_desktop.models.asset_type import AssetType
from holdings_tracker_desktop.schemas.asset_type import (
  AssetTypeCreate, AssetTypeUpdate, AssetTypeResponse
)
from holdings_tracker_desktop.repositories.base import BaseRepository
from holdings_tracker_desktop.utils.exceptions import ConflictException

class AssetTypeService:
    def __init__(self, db: Session):
        self.repository = BaseRepository[AssetType, AssetTypeCreate, AssetTypeUpdate](
            model=AssetType,
            db=db
        )

    def create(self, data: AssetTypeCreate) -> AssetTypeResponse:
        """Create new AssetType with validation"""
        if self._exists_by_name_country(data.name, data.country_id):
            raise ConflictException(
                f"AssetType '{data.name}' already exists for country ID {data.country_id}"
            )

        asset_type = self.repository.create_from_schema(data)
        return AssetTypeResponse.model_validate(asset_type)

    def get(self, asset_type_id: int) -> AssetTypeResponse:
        """Get AssetType by ID"""
        asset_type = self.repository.get_or_raise(asset_type_id)
        return AssetTypeResponse.model_validate(asset_type)

    def update(self, asset_type_id: int, data: AssetTypeUpdate) -> AssetTypeResponse:
        """Update AssetType"""
        asset_type = self.repository.get_or_raise(asset_type_id)

        if data.name and data.name != asset_type.name:
            if self._exists_by_name_country(data.name, asset_type.country_id, exclude_id=asset_type_id):
                raise ConflictException(
                    f"AssetType '{data.name}' already exists for this country"
                )

        updated = self.repository.update_from_schema(asset_type_id, data)
        return AssetTypeResponse.model_validate(updated)

    def delete(self, asset_type_id: int) -> bool:
        """Delete AssetType"""
        asset_type = self.repository.get_or_raise(asset_type_id)

        can_delete, error_message = asset_type.validate_for_deletion()
        if not can_delete:
            raise ConflictException(error_message)

        return self.repository.delete(asset_type_id)

    def list_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        order_by: str = "name",
        descending: bool = False
    ) -> List[AssetTypeResponse]:
        """List all AssetTypes"""
        asset_types = self.repository.get_all(skip, limit, order_by, descending)
        return [AssetTypeResponse.model_validate(at) for at in asset_types]

    def list_all_for_ui(
        self, 
        skip: int = 0, 
        limit: int = 100,
        order_by: str = "name",
        descending: bool = False
    ) -> List[dict]:
        """Get AssetTypes already formatted for UI"""
        asset_types = self.repository.get_all(skip, limit, order_by, descending)
        return [at.to_ui_dict() for at in asset_types]

    def count_all(self) -> int:
        """Count all AssetTypes"""
        return self.repository.count()

    def get_by_country(self, country_id: int) -> List[AssetTypeResponse]:
        """Get all AssetTypes for a country"""
        asset_types = self.repository.find_all_by(country_id=country_id)
        return [AssetTypeResponse.model_validate(at) for at in asset_types]

    def _exists_by_name_country(
        self, 
        name: str, 
        country_id: int, 
        exclude_id: Optional[int] = None
    ) -> bool:
        """Check if AssetType with name+country exists"""
        query = self.repository.db.query(AssetType).filter(
            AssetType.name.ilike(name),
            AssetType.country_id == country_id
        )

        if exclude_id:
            query = query.filter(AssetType.id != exclude_id)

        return query.first() is not None
