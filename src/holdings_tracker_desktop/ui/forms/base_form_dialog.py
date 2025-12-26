from typing import Optional
from PySide6.QtWidgets import QWidget, QDialog, QMessageBox, QVBoxLayout, QFormLayout, QDialogButtonBox
from pydantic import ValidationError

class BaseFormDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()

    def handle_validation_error(self, error: ValidationError):
        messages = []

        for err in error.errors():
            field = ".".join(map(str, err["loc"]))
            msg = err["msg"]
            messages.append(f"{field}: {msg}")

        QMessageBox.warning(
            self,
            "Validation Error",
            "\n".join(messages)
        )

    def handle_generic_error(self, error: Exception):
        QMessageBox.critical(
            self,
            "Error",
            str(error)
        )

    def _setup_ui(self):
        self.setMinimumWidth(350)
        self._main_layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()
        self._main_layout.addLayout(self._form_layout)

        self._build_form(self._form_layout)
        self._build_buttons()

    def _build_form(self, form_layout: QFormLayout): raise NotImplementedError

    def _save(self): raise NotImplementedError

    def _build_buttons(self):
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        self._main_layout.addWidget(buttons)

    def _on_accept(self):
        try:
            self._save()
            self.accept()

        except ValidationError as e:
            self.handle_validation_error(e)

        except Exception as e:
            self.handle_generic_error(e)
