from datetime import date as Date
from typing import List
from sqlalchemy.orm import Session
from holdings_tracker_desktop.models.broker_note import BrokerNote
from holdings_tracker_desktop.schemas.broker_note import (
  BrokerNoteCreate, BrokerNoteUpdate, BrokerNoteResponse
)
from holdings_tracker_desktop.repositories.base import BaseRepository

class BrokerNoteService:
    def __init__(self, db: Session):
        self.repository = BaseRepository[BrokerNote, BrokerNoteCreate, BrokerNoteUpdate](
            model=BrokerNote,
            db=db
        )

    def create(self, data: BrokerNoteCreate) -> BrokerNoteResponse:
        """Create new BrokerNote with validation"""
        broker_note = self.repository.create_from_schema(data)
        return BrokerNoteResponse.model_validate(broker_note)

    def get(self, broker_note_id: int) -> BrokerNoteResponse:
        """Get BrokerNote by ID"""
        broker_note = self.repository.get_or_raise(broker_note_id)
        return BrokerNoteResponse.model_validate(broker_note)

    def update(self, broker_note_id: int, data: BrokerNoteUpdate) -> BrokerNoteResponse:
        """Update BrokerNote"""
        updated = self.repository.update_from_schema(broker_note_id, data)
        return BrokerNoteResponse.model_validate(updated)

    def delete(self, broker_note_id: int) -> bool:
        """Delete BrokerNote"""
        return self.repository.delete(broker_note_id)

    def list_all(
        self,
        skip: int = 0, 
        limit: int = 100,
        order_by: Date = "date",
        descending: bool = True
    ) -> List[BrokerNoteResponse]:
        """List all BrokerNotes"""
        broker_notes = self.repository.get_all(skip, limit, order_by, descending)
        return [BrokerNoteResponse.model_validate(bn) for bn in broker_notes]

    def list_all_models(self, order_by: Date = "date") -> List[BrokerNote]:
        """Get all BrokerNotes as SQLAlchemy models"""
        return self.repository.get_all(order_by=order_by)

    def list_all_for_ui(
        self, 
        skip: int = 0, 
        limit: int = 100,
        order_by: Date = "date",
        descending: bool = True
    ) -> List[dict]:
        """Get BrokerNotes already formatted for UI"""
        broker_notes = self.repository.get_all(skip, limit, order_by, descending)
        return [bn.to_ui_dict() for bn in broker_notes]

    def count_all(self) -> int:
        """Count all BrokerNotes"""
        return self.repository.count()
