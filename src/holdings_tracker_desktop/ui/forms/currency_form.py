from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QVBoxLayout, QMessageBox
)
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.currency_service import CurrencyService
from holdings_tracker_desktop.schemas.currency import CurrencyCreate, CurrencyUpdate
from holdings_tracker_desktop.ui.translations import t

class CurrencyForm(QDialog):
    def __init__(self, currency_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(currency_id, initial_data)
        self._setup_ui()
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_currency") if self.is_edit_mode else t("new_currency")
        )

    def _init_state(self, currency_id, initial_data):
        self.currency_id = currency_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = currency_id is not None

    def _setup_ui(self):
        self.setMinimumWidth(350)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.code_input = QLineEdit()
        form_layout.addRow(f"{t('code')}:", self.code_input)

        self.name_input = QLineEdit()
        form_layout.addRow(f"{t('name')}:", self.name_input)

        self.symbol_input = QLineEdit()
        form_layout.addRow(f"{t('symbol')}:", self.symbol_input)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def _load_initial_data(self):
        if self.initial_data:
            self.code_input.setText(self.initial_data.get('code', ''))
            self.name_input.setText(self.initial_data.get('name', ''))
            self.symbol_input.setText(self.initial_data.get('symbol', ''))

    def _save(self):
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        symbol = self.symbol_input.text().strip()

        try:
            with get_db() as db:
                service = CurrencyService(db)

                if self.is_edit_mode:
                    update_data = CurrencyUpdate(code=code, name=name, symbol=symbol)
                    service.update(self.currency_id, update_data)
                else:
                    create_data = CurrencyCreate(code=code, name=name, symbol=symbol)
                    service.create(create_data)

                self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
