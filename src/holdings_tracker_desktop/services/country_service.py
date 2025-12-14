from typing import List, Optional
from sqlalchemy.orm import Session
from holdings_tracker_desktop.models.country import Country
from holdings_tracker_desktop.schemas.country import ( 
  CountryCreate, CountryUpdate, CountryResponse
)
from holdings_tracker_desktop.repositories.base import BaseRepository
from holdings_tracker_desktop.utils.exceptions import ConflictException

class CountryService:
    def __init__(self, db: Session):
        self.repository = BaseRepository[Country, CountryCreate, CountryUpdate](
            model=Country,
            db=db
        )

    def create(self, data: CountryCreate) -> CountryResponse:
        """Create new Country with validation"""
        country = self.repository.create_from_schema(data)
        return CountryResponse.model_validate(country)

    def get(self, country_id: int) -> CountryResponse:
        """Get Country by ID"""
        country = self.repository.get_or_raise(country_id)
        return CountryResponse.model_validate(country)

    def update(self, country_id: int, data: CountryUpdate) -> CountryResponse:
        """Update Country"""
        updated = self.repository.update_from_schema(country_id, data)
        return CountryResponse.model_validate(updated)

    def delete(self, country_id: int) -> bool:
        """Delete Country"""
        country = self.repository.get_or_raise(country_id)

        can_delete, error_message = country.validate_for_deletion()
        if not can_delete:
            raise ConflictException(error_message)

        return self.repository.delete(country_id)

    def list_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        order_by: str = "name",
        descending: bool = False
    ) -> List[CountryResponse]:
        """List all Countries"""
        countries = self.repository.get_all(skip, limit, order_by, descending)
        return [CountryResponse.model_validate(c) for c in countries]

    def list_all_models(self, order_by: str = "name") -> List[Country]:
        """Get all Countries as SQLAlchemy models"""
        return self.repository.get_all(order_by=order_by)

    def list_all_for_ui(
        self, 
        skip: int = 0, 
        limit: int = 100,
        order_by: str = "name",
        descending: bool = False
    ) -> List[dict]:
        """Get Countries already formatted for UI"""
        countries = self.repository.get_all(skip, limit, order_by, descending)
        return [c.to_ui_dict() for c in countries]

    def count_all(self) -> int:
        """Count all Countries"""
        return self.repository.count()
