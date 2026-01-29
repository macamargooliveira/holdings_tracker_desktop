from holdings_tracker_desktop.ui.comboboxes.base_year_combobox import BaseYearComboBox
from holdings_tracker_desktop.ui.core import global_signals

class BrokerNoteYearComboBox(BaseYearComboBox):
    def _connect_reload_signals(self):
        global_signals.broker_notes_updated.connect(self.reload)

    def _load_years(self) -> list[int]:
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.broker_note_service import BrokerNoteService

        with get_db() as db:
            service = BrokerNoteService(db)
            years = service.list_available_years()

        return years
