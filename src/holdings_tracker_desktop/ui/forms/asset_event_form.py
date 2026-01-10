from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDateEdit
from decimal import Decimal
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.models.asset_event import AssetEventType
from holdings_tracker_desktop.services.asset_event_service import AssetEventService
from holdings_tracker_desktop.schemas.asset_event import AssetEventCreate, AssetEventUpdate
from holdings_tracker_desktop.ui.forms.base_form_dialog import BaseFormDialog
from holdings_tracker_desktop.ui.comboboxes import AssetComboBox, EventTypeComboBox
from holdings_tracker_desktop.ui.translations import t

class AssetEventForm(BaseFormDialog):
    def __init__(self, asset_event_id=None, asset_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(asset_event_id, asset_id, initial_data)
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_asset_event") if self.is_edit_mode else t("new_asset_event")
        )

    def _init_state(self, asset_event_id, asset_id, initial_data):
        self.asset_event_id = asset_event_id
        self.asset_id = asset_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = asset_event_id is not None

    def _load_initial_data(self):
        self._load_asset(self.asset_id)

        if not self.initial_data:
            return

        data = self.initial_data

        self._load_date(data)
        self._load_event_type(data)
        self._load_financial_fields(data)

    def _load_asset(self, asset_id):
        if asset_id is None:
            return

        index = self.asset_combo.findData(asset_id)
        if index >= 0:
            self.asset_combo.setCurrentIndex(index)
            self.asset_combo.setEnabled(False)

    def _load_date(self, data: dict):
        if data.get("date"):
            qdate = QDate(data["date"])
            self.date_input.setDate(qdate)

    def _load_event_type(self, data: dict):
        event_type = data.get("event_type")
        if not event_type:
            return

        index = self.event_type_combo.findData(event_type)
        if index >= 0:
            self.event_type_combo.setCurrentIndex(index)
            self.event_type_combo.setEnabled(False)

    def _load_financial_fields(self, data: dict):
        if data.get("factor") is not None:
            self.factor_input.setValue(float(data["factor"]))

        if data.get("quantity") is not None:
            self.quantity_input.setValue(float(data["quantity"]))

        if data.get("price") is not None:
            self.price_input.setValue(float(data["price"]))

    def _build_form(self, form_layout):
        self._setup_date_input(form_layout)
        self._setup_asset_combo(form_layout)
        self._setup_event_type_combo(form_layout)
        self._setup_financial_fields(form_layout)

    def _setup_date_input(self, form_layout):
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMaximumDate(QDate.currentDate())
        form_layout.addRow(f"{t('date')}:", self.date_input)

    def _setup_asset_combo(self, form_layout):
        self.asset_combo = AssetComboBox()
        form_layout.addRow(f"{t('asset')}:", self.asset_combo)

    def _setup_event_type_combo(self, form_layout):
        self.event_type_combo = EventTypeComboBox()
        self.event_type_combo.currentIndexChanged.connect(
            self._on_event_type_changed
        )
        form_layout.addRow(f"{t('type')}:", self.event_type_combo)

    def _on_event_type_changed(self):
        event_type = self.event_type_combo.currentData()
        self._apply_event_type_ui(event_type)

    def _setup_financial_fields(self, form_layout):
        self.factor_input = self.create_decimal_spinbox()
        self.quantity_input = self.create_decimal_spinbox(decimals=0, step=1)
        self.price_input = self.create_decimal_spinbox()

        form_layout.addRow(f"{t('factor')}:", self.factor_input)
        form_layout.addRow(f"{t('quantity')}:", self.quantity_input)
        form_layout.addRow(f"{t('unit_price')}:", self.price_input)

        self._reset_event_type_fields()

    def _reset_event_type_fields(self):
        for field in (
            self.factor_input,
            self.quantity_input,
            self.price_input,
        ):
            self._form_layout.setRowVisible(field, False)
            field.setEnabled(False)
            field.setValue(0)

    def _apply_event_type_ui(self, event_type):
        self._reset_event_type_fields()

        match event_type:
            case AssetEventType.SPLIT | AssetEventType.REVERSE_SPLIT:
                self._form_layout.setRowVisible(self.factor_input, True)
                self.factor_input.setEnabled(True)

            case AssetEventType.AMORTIZATION | AssetEventType.SUBSCRIPTION:
                self._form_layout.setRowVisible(self.quantity_input, True)
                self._form_layout.setRowVisible(self.price_input, True)
                self.quantity_input.setEnabled(True)
                self.price_input.setEnabled(True)

    def _save(self):
        asset_id = self.asset_id
        event_type =  self.event_type_combo.currentData()
        date = self.date_input.date().toPython()

        factor = quantity = price = None

        match event_type:
            case AssetEventType.SPLIT | AssetEventType.REVERSE_SPLIT:
                factor = Decimal(str(self.factor_input.value()))

            case AssetEventType.AMORTIZATION | AssetEventType.SUBSCRIPTION:
                quantity = Decimal(str(self.quantity_input.value()))
                price = Decimal(str(self.price_input.value()))

        with get_db() as db:
            service = AssetEventService(db)

            if self.is_edit_mode:
                update_data = AssetEventUpdate(
                    asset_id=asset_id,
                    event_type=event_type,
                    date=date, 
                    factor=factor,
                    quantity=quantity,
                    price=price
                )
                service.update(self.asset_event_id, update_data)
            else:
                create_data = AssetEventCreate(
                    asset_id=asset_id,
                    event_type=event_type,
                    date=date,
                    factor=factor,
                    quantity=quantity,
                    price=price
                )
                service.create(create_data)
