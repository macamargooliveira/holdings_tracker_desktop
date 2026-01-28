from PySide6.QtWidgets import QLineEdit

from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.schemas.country import CountryCreate, CountryUpdate
from holdings_tracker_desktop.services.country_service import CountryService
from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.forms.base_form_dialog import BaseFormDialog

class CountryForm(BaseFormDialog):
    def __init__(self, country_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(country_id, initial_data)
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_country") if self.is_edit_mode else t("new_country")
        )

    def _init_state(self, country_id, initial_data):
        self.country_id = country_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = country_id is not None

    def _load_initial_data(self):
        if not self.initial_data:
            return
        
        data = self.initial_data

        self._load_name(data)

    def _load_name(self, data: dict):
        if data.get('name'):
            self.name_input.setText(data['name'])

    def _build_form(self, form_layout):
        self._setup_name_input(form_layout)

    def _setup_name_input(self, form_layout):
        self.name_input = QLineEdit()
        form_layout.addRow(f"{t('name')}:", self.name_input)

    def _save(self):
        name = self.name_input.text().strip()

        with get_db() as db:
            service = CountryService(db)

            if self.is_edit_mode:
                update_data = CountryUpdate(name=name)
                service.update(self.country_id, update_data)
            else:
                create_data = CountryCreate(name=name)
                service.create(create_data)
