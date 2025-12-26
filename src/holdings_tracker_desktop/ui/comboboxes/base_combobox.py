from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox
from holdings_tracker_desktop.ui.translations import t

class BaseComboBox(QComboBox):
    def __init__(self, placeholder_key: str, parent=None):
        super().__init__(parent)

        self.placeholder_key = placeholder_key

        self.setEditable(False)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setFocusPolicy(Qt.StrongFocus)

        self._setup_placeholder()

    def _setup_placeholder(self):
        self.clear()
        self.addItem(t(self.placeholder_key), None)

    def reload(self): raise NotImplementedError
