from PySide6.QtWidgets import QLineEdit

from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.schemas.asset_ticker_history import AssetTickerHistoryCreate
from holdings_tracker_desktop.services.asset_ticker_history_service import AssetTickerHistoryService
from holdings_tracker_desktop.ui.comboboxes import AssetComboBox
from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.forms.base_form_dialog import BaseFormDialog
from holdings_tracker_desktop.ui.forms.date_input import DateInput

class AssetTickerHistoryForm(BaseFormDialog):
    def __init__(self, asset_id: int, parent=None):
        super().__init__(parent)
        self.asset_id = asset_id
        self._load_asset(self.asset_id)
        self.setWindowTitle(t("new_asset_ticker_history"))

    def _load_asset(self, asset_id):
        if asset_id is None:
            return

        index = self.asset_combo.findData(asset_id)
        if index >= 0:
            self.asset_combo.setCurrentIndex(index)
            self.asset_combo.setEnabled(False)

    def _build_form(self, form_layout):
        self._setup_change_date_input(form_layout)
        self._setup_asset_combo(form_layout)
        self._setup_new_ticker(form_layout)

    def _setup_change_date_input(self, form_layout):
        self.change_date_input = DateInput()
        form_layout.addRow(f"{t('change_date')}:", self.change_date_input)

    def _setup_asset_combo(self, form_layout):
        self.asset_combo = AssetComboBox()
        form_layout.addRow(f"{t('asset')}:", self.asset_combo)

    def _setup_new_ticker(self, form_layout):
        self.new_ticker_input = QLineEdit()
        form_layout.addRow(f"{t('new_ticker')}:", self.new_ticker_input)

    def _save(self):
        change_date = self.change_date_input.date().toPython()
        asset_id = self.asset_combo.currentData()
        new_ticker = self.new_ticker_input.text().strip()

        with get_db() as db:
            service = AssetTickerHistoryService(db)

            create_data = AssetTickerHistoryCreate(
                change_date=change_date, 
                asset_id=asset_id, 
                new_ticker=new_ticker
            )
            service.create(create_data)
