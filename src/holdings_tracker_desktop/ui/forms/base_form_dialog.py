from pydantic import ValidationError
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
  QWidget, QDialog, QMessageBox, QVBoxLayout, QFormLayout, QDialogButtonBox, QDoubleSpinBox
)

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

    def create_decimal_spinbox(
            self, 
            decimals: int = 2, 
            minimum: float = 0.0, 
            maximum: float = 10**12,
            step: float = 0.01,
            default: float = 0.0
        ) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setDecimals(decimals)
        spin.setMinimum(minimum)
        spin.setMaximum(maximum)
        spin.setSingleStep(step)
        spin.setValue(default)
        spin.setAlignment(Qt.AlignRight)
        spin.setButtonSymbols(QDoubleSpinBox.NoButtons)
        return spin

    def _setup_ui(self):
        self.setMinimumWidth(350)
        self._main_layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()
        self._main_layout.addLayout(self._form_layout)

        self._build_form(self._form_layout)
        self._build_buttons()

    def _build_form(self, form_layout: QFormLayout):
        pass

    def _save(self):
        pass

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
