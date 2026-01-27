from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QCompleter
from holdings_tracker_desktop.ui.translations import t

class BaseComboBox(QComboBox):
    def __init__(
        self,
        placeholder_key: str, 
        parent=None, 
        *, 
        searchable: bool = False,
        max_visible_items: int = 15
    ):
        super().__init__(parent)

        self.placeholder_key = placeholder_key

        self.setInsertPolicy(QComboBox.NoInsert)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMaxVisibleItems(max_visible_items)
        self.set_searchable(searchable)

        self._setup_placeholder()

    def set_searchable(self, enabled: bool):
        self.setEditable(enabled)

        if not enabled:
            self.setCompleter(None)
            return

        completer = QCompleter(self.model(), self)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(completer)

    def _setup_placeholder(self):
        self.clear()
        self.addItem(t(self.placeholder_key), None)

    def reload(self): raise NotImplementedError
