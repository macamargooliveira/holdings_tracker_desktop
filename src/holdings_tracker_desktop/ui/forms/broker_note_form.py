from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import QWidget, QDateEdit, QButtonGroup, QRadioButton, QHBoxLayout, QDoubleSpinBox
from decimal import Decimal
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.models.broker_note import OperationType
from holdings_tracker_desktop.services.broker_note_service import BrokerNoteService
from holdings_tracker_desktop.schemas.broker_note import BrokerNoteCreate, BrokerNoteUpdate
from holdings_tracker_desktop.ui.forms.base_form_dialog import BaseFormDialog
from holdings_tracker_desktop.ui.comboboxes import AssetComboBox, BrokerComboBox
from holdings_tracker_desktop.ui.translations import t

class BrokerNoteForm(BaseFormDialog):
    def __init__(self, broker_note_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(broker_note_id, initial_data)
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_broker_note") if self.is_edit_mode else t("new_broker_note")
        )

    def _init_state(self, broker_note_id, initial_data):
        self.broker_note_id = broker_note_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = broker_note_id is not None

    def _load_initial_data(self):
        if not self.initial_data:
            return
        
        data = self.initial_data

        self._load_date(data)
        self._load_operation(data)
        self._load_broker(data)
        self._load_asset(data)
        self._load_financial_fields(data)

    def _load_date(self, data: dict):
        if data.get("date"):
            qdate = QDate(data["date"])
            self.date_input.setDate(qdate)

    def _load_operation(self, data: dict):
        operation = data.get("operation")

        if operation == OperationType.BUY:
            self.buy_radio.setChecked(True)
        elif operation == OperationType.SELL:
            self.sell_radio.setChecked(True)

    def _load_broker(self, data: dict):
        broker_id = data.get("broker_id")

        if broker_id is None:
            return

        index = self.broker_combo.findData(broker_id)
        if index >= 0:
            self.broker_combo.setCurrentIndex(index)

    def _load_asset(self, data: dict):
        asset_id = data.get("asset_id")

        if asset_id is None:
            return

        index = self.asset_combo.findData(asset_id)
        if index >= 0:
            self.asset_combo.setCurrentIndex(index)

    def _load_financial_fields(self, data: dict):
        if data.get("quantity") is not None:
            self.quantity_input.setValue(float(data["quantity"]))

        if data.get("price") is not None:
            self.price_input.setValue(float(data["price"]))

        if data.get("fees") is not None:
            self.fees_input.setValue(float(data["fees"]))

        if data.get("taxes") is not None:
            self.taxes_input.setValue(float(data["taxes"]))

    def _build_form(self, form_layout):
        self._setup_date_input(form_layout)
        self._setup_operation_radio_button(form_layout)
        self._setup_broker_combo(form_layout)
        self._setup_asset_combo(form_layout)
        self._setup_financial_fields(form_layout)

    def _setup_date_input(self, form_layout):
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMaximumDate(QDate.currentDate())
        form_layout.addRow(f"{t('date')}:", self.date_input)

    def _setup_operation_radio_button(self, form_layout):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.operation_group = QButtonGroup(self)

        self.buy_radio = QRadioButton(t('buy'))
        self.buy_radio.setProperty('value', OperationType.BUY)
        self.operation_group.addButton(self.buy_radio)

        self.sell_radio = QRadioButton(t('sell'))
        self.sell_radio.setProperty('value', OperationType.SELL)
        self.operation_group.addButton(self.sell_radio)

        self.buy_radio.setChecked(True)

        layout.addWidget(self.buy_radio)
        layout.addWidget(self.sell_radio)
        layout.addStretch()

        form_layout.addRow(f"{t('operation')}:", container)

    def _setup_broker_combo(self, form_layout):
        self.broker_combo = BrokerComboBox()
        if self.broker_combo.count() > 1:
          self.broker_combo.setCurrentIndex(1)
        form_layout.addRow(f"{t('broker')}:", self.broker_combo)

    def _setup_asset_combo(self, form_layout):
        self.asset_combo = AssetComboBox()
        form_layout.addRow(f"{t('asset')}:", self.asset_combo)

    def _setup_financial_fields(self, form_layout):
        self.quantity_input = self._create_decimal_spinbox(decimals=0, step=1)
        self.price_input = self._create_decimal_spinbox()
        self.fees_input = self._create_decimal_spinbox()
        self.taxes_input = self._create_decimal_spinbox()

        form_layout.addRow(f"{t('quantity')}:", self.quantity_input)
        form_layout.addRow(f"{t('price')}:", self.price_input)
        form_layout.addRow(f"{t('fees')}:", self.fees_input)
        form_layout.addRow(f"{t('taxes')}:", self.taxes_input)

    def _create_decimal_spinbox(
            self, 
            decimals: int = 2, 
            minimum: float = 0.0, 
            maximum: float = 10**12,
            step: float = 0.01,
            default: float = 0.0
        ) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setDecimals(decimals)
        spin.setMinimum(minimum)
        spin.setMaximum(maximum)
        spin.setSingleStep(step)
        spin.setValue(default)
        spin.setAlignment(Qt.AlignRight)
        spin.setButtonSymbols(QDoubleSpinBox.NoButtons)
        return spin

    def _save(self):
        date = self.date_input.date().toPython()
        operation: OperationType = self.operation_group.checkedButton().property("value")
        broker_id = self.broker_combo.currentData()
        asset_id = self.asset_combo.currentData()
        quantity = Decimal(str(self.quantity_input.value()))
        price = Decimal(str(self.price_input.value()))
        fees = Decimal(str(self.fees_input.value()))
        taxes = Decimal(str(self.taxes_input.value()))

        with get_db() as db:
            service = BrokerNoteService(db)

            if self.is_edit_mode:
                update_data = BrokerNoteUpdate(
                    date=date, 
                    operation=operation, 
                    broker_id=broker_id,
                    asset_id=asset_id,
                    quantity=quantity,
                    price=price,
                    fees=fees,
                    taxes=taxes
                )
                service.update(self.broker_note_id, update_data)
            else:
                create_data = BrokerNoteCreate(
                    date=date, 
                    operation=operation, 
                    broker_id=broker_id,
                    asset_id=asset_id,
                    quantity=quantity,
                    price=price,
                    fees=fees,
                    taxes=taxes
                )
                service.create(create_data)
