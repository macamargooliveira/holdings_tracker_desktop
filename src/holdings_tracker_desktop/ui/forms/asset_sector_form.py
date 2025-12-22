from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, 
    QDialogButtonBox, QVBoxLayout, QMessageBox
)
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_sector_service import AssetSectorService
from holdings_tracker_desktop.schemas.asset_sector import AssetSectorCreate, AssetSectorUpdate
from holdings_tracker_desktop.ui.translations import t

class AssetSectorForm(QDialog):
    def __init__(self, asset_sector_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(asset_sector_id, initial_data)
        self._setup_ui()
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_asset_sector") if self.is_edit_mode else t("new_asset_sector")
        )

    def _init_state(self, asset_sector_id, initial_data):
        self.asset_sector_id = asset_sector_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = asset_sector_id is not None

    def _setup_ui(self):
        self.setMinimumWidth(350)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        form_layout.addRow(f"{t('name')}:", self.name_input)

        self.asset_type_combo = QComboBox()
        self.asset_type_combo.setEditable(False)
        self.asset_type_combo.setInsertPolicy(QComboBox.NoInsert)
        self.asset_type_combo.setFocusPolicy(Qt.StrongFocus)
        self._load_asset_types()
        form_layout.addRow(f"{t('asset_type')}:", self.asset_type_combo)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def _load_initial_data(self):
        if self.initial_data:
            self.name_input.setText(self.initial_data.get('name', ''))

            asset_type_id = self.initial_data.get('asset_type_id')
            if asset_type_id:
                for i in range(self.asset_type_combo.count()):
                    if self.asset_type_combo.itemData(i) == asset_type_id:
                        self.asset_type_combo.setCurrentIndex(i)
                        break

    def _load_asset_types(self):
        try:
            with get_db() as db:
                from holdings_tracker_desktop.services.asset_type_service import AssetTypeService

                service = AssetTypeService(db)
                asset_types = service.list_all_models()

                self.asset_type_combo.addItem(t("select_asset_type"), None)
                for asset_type in asset_types:
                    self.asset_type_combo.addItem(asset_type.name, asset_type.id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading asset types: {str(e)}")

    def _save(self):
        name = self.name_input.text().strip()
        asset_type_id = self.asset_type_combo.currentData()

        try:
            with get_db() as db:
                service = AssetSectorService(db)

                if self.is_edit_mode:
                    update_data = AssetSectorUpdate(name=name, asset_type_id=asset_type_id)
                    service.update(self.asset_sector_id, update_data)
                else:
                    create_data = AssetSectorCreate(name=name, asset_type_id=asset_type_id)
                    service.create(create_data)

                self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
