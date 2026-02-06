from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox, QLabel

from holdings_tracker_desktop.ui.core import t

class BaseDetailsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self._main_layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()
        self._form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._main_layout.addLayout(self._form_layout)

        self._build_buttons()

    def _build_buttons(self):
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.button(QDialogButtonBox.Close).setText(t("close"))
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)

        self._main_layout.addWidget(buttons)

    def add_detail(self, label: str, value: str | None):
        value_label = QLabel(value or "")
        value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self._form_layout.addRow(f"{label}:", value_label)
