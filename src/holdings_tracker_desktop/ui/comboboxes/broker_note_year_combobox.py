from PySide6.QtCore import Qt

from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox
from holdings_tracker_desktop.ui.core import t, global_signals

class BrokerNoteYearComboBox(BaseComboBox):
    """
    This ComboBox controls when BrokerNotesWidget reloads data.

    On broker_notes_updated:
    - reloads available years
    - adjusts current index
    - emits currentIndexChanged
    """

    def __init__(self, parent=None):
        super().__init__("select_year", parent, searchable=True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setObjectName("BrokerNoteYearComboBox")
        self.reload()

        global_signals.broker_notes_updated.connect(self.reload)

    def reload(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.broker_note_service import BrokerNoteService

        self.blockSignals(True)
        self.clear()

        self._setup_placeholder()

        with get_db() as db:
            service = BrokerNoteService(db)
            years = service.list_available_years()

            for year in years:
                self.addItem(str(year), year)

        if years and self.count() > 1:
            self.setCurrentIndex(1)

        self.blockSignals(False)

        self.currentIndexChanged.emit(self.currentIndex())

    def translate_placeholder(self):
        self.setItemText(0, t(self.placeholder_key))
