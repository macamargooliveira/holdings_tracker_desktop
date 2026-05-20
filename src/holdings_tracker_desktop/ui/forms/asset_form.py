from PySide6.QtWidgets import QLineEdit

from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.schemas.asset import AssetCreate, AssetUpdate
from holdings_tracker_desktop.services.asset_service import AssetService
from holdings_tracker_desktop.ui.comboboxes import AssetTypeComboBox, CurrencyComboBox, AssetSectorComboBox
from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.forms.base_form_dialog import BaseFormDialog

class AssetForm(BaseFormDialog):
    def __init__(self, asset_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(asset_id, initial_data)
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_asset") if self.is_edit_mode else t("new_asset")
        )

    def _init_state(self, asset_id, initial_data):
        self.asset_id = asset_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = asset_id is not None

    def _load_initial_data(self):
        if not self.initial_data:
            return

        data = self.initial_data

        self._load_ticker(data)
        self._load_type(data)

        # After setting the type, populate the sector combo filtered by that type
        # so that `_load_sector` can select the correct sector if present.
        try:
            # call handler with current index (signal usually passes an int)
            self._on_type_changed(self.type_combo.currentIndex())
        except Exception:
            # defensive: if combo not ready or handler missing, ignore
            pass

        self._load_currency(data)
        self._load_sector(data)

    def _load_ticker(self, data: dict):
        if data.get('ticker'):
            self.ticker_input.setText(data['ticker'])
            self.ticker_input.setEnabled(False)

    def _load_type(self, data: dict):
        type_id = data.get('type_id')

        if type_id is None:
            return

        index = self.type_combo.findData(type_id)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)

    def _load_currency(self, data: dict):
        currency_id = data.get('currency_id')

        if currency_id is None:
            return

        index = self.currency_combo.findData(currency_id)
        if index >= 0:
            self.currency_combo.setCurrentIndex(index)

    def _load_sector(self, data: dict):
        sector_id = data.get('sector_id')

        if sector_id is None:
            return

        index = self.sector_combo.findData(sector_id)
        if index >= 0:
            self.sector_combo.setCurrentIndex(index)

    def _build_form(self, form_layout):
        self._setup_ticker_input(form_layout)
        self._setup_type_combo(form_layout)
        self._setup_currency_combo(form_layout)
        self._setup_sector_combo(form_layout)

    def _setup_ticker_input(self, form_layout):
        self.ticker_input = QLineEdit()
        form_layout.addRow(f"{t('ticker')}:", self.ticker_input)

    def _setup_type_combo(self, form_layout):
        self.type_combo = AssetTypeComboBox()
        # update sectors when the selected type changes
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        form_layout.addRow(f"{t('type')}:", self.type_combo)

    def _setup_currency_combo(self, form_layout):
        self.currency_combo = CurrencyComboBox()
        form_layout.addRow(f"{t('currency')}:", self.currency_combo)

    def _setup_sector_combo(self, form_layout):
        self.sector_combo = AssetSectorComboBox()
        form_layout.addRow(f"{t('sector')}:", self.sector_combo)

    def _on_type_changed(self, index=None):
        """Handler called when asset type changes. Reloads sectors for the
        selected type and clears sector selection if current sector is not
        present in the new list.
        """
        # remember previously selected sector id
        prev_sector_id = self.sector_combo.currentData()

        # get currently selected type id
        type_id = self.type_combo.currentData()

        # reload sector options filtered by type
        self.sector_combo.load_for_type(type_id)

        # if there was a previously selected sector, try to restore it
        if prev_sector_id is None:
            return

        idx = self.sector_combo.findData(prev_sector_id)
        if idx >= 0:
            self.sector_combo.setCurrentIndex(idx)
        else:
            # clear selection (set to placeholder)
            self.sector_combo.setCurrentIndex(0)

    def _save(self):
        ticker = self.ticker_input.text().strip()
        type_id = self.type_combo.currentData()
        currency_id = self.currency_combo.currentData()
        sector_id = self.sector_combo.currentData()

        with get_db() as db:
            service = AssetService(db)

            if self.is_edit_mode:
                update_data = AssetUpdate(
                    type_id=type_id, 
                    currency_id=currency_id, 
                    sector_id=sector_id
                )
                service.update(self.asset_id, update_data)
            else:
                create_data = AssetCreate(
                    ticker=ticker, 
                    type_id=type_id, 
                    currency_id=currency_id, 
                    sector_id=sector_id
                )
                service.create(create_data)
