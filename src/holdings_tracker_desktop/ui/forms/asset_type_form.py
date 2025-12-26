from PySide6.QtWidgets import QLineEdit
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_type_service import AssetTypeService
from holdings_tracker_desktop.schemas.asset_type import AssetTypeCreate, AssetTypeUpdate
from holdings_tracker_desktop.ui.forms.base_form_dialog import BaseFormDialog
from holdings_tracker_desktop.ui.comboboxes import CountryComboBox
from holdings_tracker_desktop.ui.translations import t

class AssetTypeForm(BaseFormDialog):
    def __init__(self, asset_type_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(asset_type_id, initial_data)
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_asset_type") if self.is_edit_mode else t("new_asset_type")
        )

    def _init_state(self, asset_type_id, initial_data):
        self.asset_type_id = asset_type_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = asset_type_id is not None

    def _load_initial_data(self):
        if not self.initial_data:
            return

        data = self.initial_data

        self._load_name(data)
        self._load_country(data)

    def _load_name(self, data: dict):
        if data.get('name'):
            self.name_input.setText(data['name'])

    def _load_country(self, data: dict):
        country_id = data.get('country_id')

        if country_id is None:
            return

        index = self.country_combo.findData(country_id)
        if index >= 0:
            self.country_combo.setCurrentIndex(index)

    def _build_form(self, form_layout):
        self._setup_name_input(form_layout)
        self._setup_country_combo(form_layout)

    def _setup_name_input(self, form_layout):
        self.name_input = QLineEdit()
        form_layout.addRow(f"{t('name')}:", self.name_input)

    def _setup_country_combo(self, form_layout):
        self.country_combo = CountryComboBox()
        form_layout.addRow(f"{t('country')}:", self.country_combo)

    def _save(self):
        name = self.name_input.text().strip()
        country_id = self.country_combo.currentData()

        with get_db() as db:
            service = AssetTypeService(db)

            if self.is_edit_mode:
                update_data = AssetTypeUpdate(
                    name=name, 
                    country_id=country_id
                )
                service.update(self.asset_type_id, update_data)
            else:
                create_data = AssetTypeCreate(
                    name=name, 
                    country_id=country_id
                )
                service.create(create_data)
