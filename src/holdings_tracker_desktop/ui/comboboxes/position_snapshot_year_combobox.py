from datetime import date as Date

from holdings_tracker_desktop.ui.comboboxes.base_year_combobox import BaseYearComboBox
from holdings_tracker_desktop.ui.core import global_signals

class PositionSnapshotYearComboBox(BaseYearComboBox):
    def _connect_reload_signals(self):
        global_signals.asset_events_updated.connect(self.reload)
        global_signals.broker_notes_updated.connect(self.reload)

    def _load_years(self) -> list[int]:
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.position_snapshot_service import PositionSnapshotService

        with get_db() as db:
            service = PositionSnapshotService(db)
            min_date = service.get_earliest_snapshot_date()

        current_year = Date.today().year
        start_year = min_date.year if min_date else current_year
        return list(range(current_year, start_year - 1, -1))
