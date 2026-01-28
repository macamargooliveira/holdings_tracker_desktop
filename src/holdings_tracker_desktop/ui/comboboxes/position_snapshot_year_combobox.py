from datetime import date as Date

from PySide6.QtCore import Qt

from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox
from holdings_tracker_desktop.ui.core import t, global_signals

class PositionSnapshotYearComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_year", parent, searchable=True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setObjectName("YearComboBox")
        self.reload()

        global_signals.asset_events_updated.connect(self.reload)
        global_signals.broker_notes_updated.connect(self.reload)

    def reload(self):
        self.blockSignals(True)
        self.clear()

        self._setup_placeholder()

        for year in self._load_years():
            self.addItem(str(year), year)

        if self.count() > 1:
            self.setCurrentIndex(1)

        self.blockSignals(False)
        self.currentIndexChanged.emit(self.currentIndex())

    def translate_placeholder(self):
        self.setItemText(0, t(self.placeholder_key))

    def _load_years(self) -> list[int]:
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.position_snapshot_service import PositionSnapshotService

        with get_db() as db:
            service = PositionSnapshotService(db)
            min_date = service.get_earliest_snapshot_date()

        current_year = Date.today().year
        start_year = min_date.year if min_date else current_year
        return list(range(current_year, start_year - 1, -1))
