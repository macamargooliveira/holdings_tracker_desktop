from PySide6.QtWidgets import QLineEdit
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_sector_service import AssetSectorService
from holdings_tracker_desktop.schemas.asset_sector import AssetSectorCreate, AssetSectorUpdate
from holdings_tracker_desktop.ui.forms.base_form_dialog import BaseFormDialog
from holdings_tracker_desktop.ui.comboboxes import AssetTypeComboBox
from holdings_tracker_desktop.ui.translations import t

class AssetSectorForm(BaseFormDialog):
    def __init__(self, asset_sector_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(asset_sector_id, initial_data)
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_asset_sector") if self.is_edit_mode else t("new_asset_sector")
        )

    def _init_state(self, asset_sector_id, initial_data):
        self.asset_sector_id = asset_sector_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = asset_sector_id is not None

    def _load_initial_data(self):
        if not self.initial_data:
            return

        data = self.initial_data

        self._load_name(data)
        self._load_asset_type(data)

    def _load_name(self, data: dict):
        if data.get('name'):
            self.name_input.setText(data['name'])

    def _load_asset_type(self, data: dict):
        asset_type_id = data.get('asset_type_id')

        if asset_type_id is None:
            return

        index = self.asset_type_combo.findData(asset_type_id)
        if index >= 0:
            self.asset_type_combo.setCurrentIndex(index)

    def _build_form(self, form_layout):
        self._setup_name_input(form_layout)
        self._setup_asset_type_combo(form_layout)

    def _setup_name_input(self, form_layout):
        self.name_input = QLineEdit()
        form_layout.addRow(f"{t('name')}:", self.name_input)

    def _setup_asset_type_combo(self, form_layout):
        self.asset_type_combo = AssetTypeComboBox()
        form_layout.addRow(f"{t('asset_type')}:", self.asset_type_combo)

    def _save(self):
        name = self.name_input.text().strip()
        asset_type_id = self.asset_type_combo.currentData()

        with get_db() as db:
            service = AssetSectorService(db)

            if self.is_edit_mode:
                update_data = AssetSectorUpdate(
                    name=name, 
                    asset_type_id=asset_type_id
                )
                service.update(self.asset_sector_id, update_data)
            else:
                create_data = AssetSectorCreate(
                    name=name, 
                    asset_type_id=asset_type_id
                )
                service.create(create_data)
