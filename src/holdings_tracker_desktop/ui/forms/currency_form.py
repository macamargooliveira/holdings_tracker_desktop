from PySide6.QtWidgets import QLineEdit
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.currency_service import CurrencyService
from holdings_tracker_desktop.schemas.currency import CurrencyCreate, CurrencyUpdate
from holdings_tracker_desktop.ui.forms.base_form_dialog import BaseFormDialog
from holdings_tracker_desktop.ui.translations import t

class CurrencyForm(BaseFormDialog):
    def __init__(self, currency_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(currency_id, initial_data)
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_currency") if self.is_edit_mode else t("new_currency")
        )

    def _init_state(self, currency_id, initial_data):
        self.currency_id = currency_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = currency_id is not None

    def _load_initial_data(self):
        if not self.initial_data:
            return
        
        data = self.initial_data

        self._load_code(data)
        self._load_name(data)
        self._load_symbol(data)

    def _load_code(self, data: dict):
        if data.get('code'):
            self.code_input.setText(data['code'])

    def _load_name(self, data: dict):
        if data.get('name'):
            self.name_input.setText(data['name'])

    def _load_symbol(self, data: dict):
        if data.get('symbol'):
            self.symbol_input.setText(data['symbol'])

    def _build_form(self, form_layout):
        self._setup_code_input(form_layout)
        self._setup_name_input(form_layout)
        self._setup_symbol_input(form_layout)

    def _setup_code_input(self, form_layout):
        self.code_input = QLineEdit()
        form_layout.addRow(f"{t('code')}:", self.code_input)

    def _setup_name_input(self, form_layout):
        self.name_input = QLineEdit()
        form_layout.addRow(f"{t('name')}:", self.name_input)

    def _setup_symbol_input(self, form_layout):
        self.symbol_input = QLineEdit()
        form_layout.addRow(f"{t('symbol')}:", self.symbol_input)

    def _save(self):
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        symbol = self.symbol_input.text().strip()

        with get_db() as db:
            service = CurrencyService(db)

            if self.is_edit_mode:
                update_data = CurrencyUpdate(
                    code=code, 
                    name=name, 
                    symbol=symbol
                )
                service.update(self.currency_id, update_data)
            else:
                create_data = CurrencyCreate(
                    code=code, 
                    name=name, 
                    symbol=symbol
                )
                service.create(create_data)
