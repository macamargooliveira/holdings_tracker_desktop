from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, 
    QDialogButtonBox, QVBoxLayout, QMessageBox
)
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_service import AssetService
from holdings_tracker_desktop.schemas.asset import AssetCreate, AssetUpdate
from holdings_tracker_desktop.ui.translations import t

class AssetForm(QDialog):
    def __init__(self, asset_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(asset_id, initial_data)
        self._setup_ui()
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_asset") if self.is_edit_mode else t("new_asset")
        )

    def _init_state(self, asset_id, initial_data):
        self.asset_id = asset_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = asset_id is not None

    def _setup_ui(self):
        self.setMinimumWidth(350)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.ticker_input = QLineEdit()
        form_layout.addRow(f"{t('ticker')}:", self.ticker_input)

        self._setup_type_combo(form_layout)
        self._setup_currency_combo(form_layout)
        self._setup_sector_combo(form_layout)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def _load_initial_data(self):
        if self.initial_data:
            self.ticker_input.setText(self.initial_data.get('ticker', ''))

            type_id = self.initial_data.get('type_id')
            if type_id:
                for i in range(self.type_combo.count()):
                    if self.type_combo.itemData(i) == type_id:
                        self.type_combo.setCurrentIndex(i)
                        break

            currency_id = self.initial_data.get('currency_id')
            if currency_id:
                for i in range(self.currency_combo.count()):
                    if self.currency_combo.itemData(i) == currency_id:
                        self.currency_combo.setCurrentIndex(i)
                        break

            sector_id = self.initial_data.get('sector_id')
            if sector_id:
                for i in range(self.sector_combo.count()):
                    if self.sector_combo.itemData(i) == sector_id:
                        self.sector_combo.setCurrentIndex(i)
                        break
    
    def _setup_type_combo(self, form_layout):
        self.type_combo = QComboBox()
        self.type_combo.setEditable(False)
        self.type_combo.setInsertPolicy(QComboBox.NoInsert)
        self.type_combo.setFocusPolicy(Qt.StrongFocus)
        self._load_asset_types()
        form_layout.addRow(f"{t('type')}:", self.type_combo)

    def _load_asset_types(self):
        try:
            with get_db() as db:
                from holdings_tracker_desktop.services.asset_type_service import AssetTypeService

                service = AssetTypeService(db)
                asset_types = service.list_all_models()

                self.type_combo.addItem(t("select_asset_type"), None)
                for asset_type in asset_types:
                    self.type_combo.addItem(asset_type.name, asset_type.id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading asset types: {str(e)}")

    def _setup_currency_combo(self, form_layout):
        self.currency_combo = QComboBox()
        self.currency_combo.setEditable(False)
        self.currency_combo.setInsertPolicy(QComboBox.NoInsert)
        self.currency_combo.setFocusPolicy(Qt.StrongFocus)
        self._load_currencies()
        form_layout.addRow(f"{t('currency')}:", self.currency_combo)

    def _load_currencies(self):
        try:
            with get_db() as db:
                from holdings_tracker_desktop.services.currency_service import CurrencyService

                service = CurrencyService(db)
                currencies = service.list_all_models()

                self.currency_combo.addItem(t("select_currency"), None)
                for currency in currencies:
                    self.currency_combo.addItem(currency.code, currency.id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading currencies: {str(e)}")

    def _setup_sector_combo(self, form_layout):
        self.sector_combo = QComboBox()
        self.sector_combo.setEditable(False)
        self.sector_combo.setInsertPolicy(QComboBox.NoInsert)
        self.sector_combo.setFocusPolicy(Qt.StrongFocus)
        self._load_asset_sectors()
        form_layout.addRow(f"{t('sector')}:", self.sector_combo)

    def _load_asset_sectors(self):
        try:
            with get_db() as db:
                from holdings_tracker_desktop.services.asset_sector_service import AssetSectorService

                service = AssetSectorService(db)
                sectors = service.list_all_models()

                self.sector_combo.addItem(t("select_sector"), None)
                for sector in sectors:
                    self.sector_combo.addItem(sector.name, sector.id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading sectors: {str(e)}")

    def _save(self):
        ticker = self.ticker_input.text().strip()
        type_id = self.type_combo.currentData()
        currency_id = self.currency_combo.currentData()
        sector_id = self.sector_combo.currentData()

        try:
            with get_db() as db:
                service = AssetService(db)

                if self.is_edit_mode:
                    update_data = AssetUpdate(type_id=type_id, currency_id=currency_id, sector_id=sector_id)
                    service.update(self.asset_id, update_data)
                else:
                    create_data = AssetCreate(ticker=ticker, type_id=type_id, currency_id=currency_id, sector_id=sector_id)
                    service.create(create_data)

                self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
