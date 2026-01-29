from PySide6.QtCore import Qt

from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox
from holdings_tracker_desktop.ui.core import t

class BaseYearComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_year", parent, searchable=True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setObjectName("YearComboBox")
        self._connect_reload_signals()
        self.reload()

    def _connect_reload_signals(self):
        pass

    def _load_years(self) -> list[int]:
        pass

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
        self.setItemText(0, f" {t(self.placeholder_key)}")
