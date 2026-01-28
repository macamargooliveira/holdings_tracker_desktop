from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

from holdings_tracker_desktop.ui.core import t

class ConfirmDialog(QDialog):
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.message = message
        self._setup_ui()

    def _setup_ui(self):
        self.setMinimumWidth(350)
        self.setWindowTitle(self.title)

        layout = QVBoxLayout(self)

        label = QLabel(self.message)
        layout.addWidget(label)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        buttons.button(QDialogButtonBox.Ok).setText(t("yes"))
        buttons.button(QDialogButtonBox.Cancel).setText(t("no"))

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        buttons.button(QDialogButtonBox.Cancel).setDefault(True)
        buttons.button(QDialogButtonBox.Cancel).setFocus()
