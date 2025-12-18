from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, 
    QDialogButtonBox, QVBoxLayout, QMessageBox
)
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.broker_service import BrokerService
from holdings_tracker_desktop.schemas.broker import BrokerCreate, BrokerUpdate
from holdings_tracker_desktop.ui.translations import t

class BrokerForm(QDialog):
    def __init__(self, broker_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(broker_id, initial_data)
        self._setup_ui()
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_broker") if self.is_edit_mode else t("new_broker")
        )

    def _init_state(self, broker_id, initial_data):
        self.broker_id = broker_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = broker_id is not None

    def _setup_ui(self):
        self.setMinimumWidth(350)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        form_layout.addRow(f"{t('name')}:", self.name_input)

        self.country_combo = QComboBox()
        self.country_combo.setEditable(False)
        self.country_combo.setInsertPolicy(QComboBox.NoInsert)
        self.country_combo.setFocusPolicy(Qt.StrongFocus)
        self._load_countries()
        form_layout.addRow(f"{t('country')}:", self.country_combo)

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

            country_id = self.initial_data.get('country_id')
            if country_id:
                for i in range(self.country_combo.count()):
                    if self.country_combo.itemData(i) == country_id:
                        self.country_combo.setCurrentIndex(i)
                        break

    def _load_countries(self):
        try:
            with get_db() as db:
                from holdings_tracker_desktop.services.country_service import CountryService

                service = CountryService(db)
                countries = service.list_all_models(order_by="name")

                self.country_combo.addItem(t("select_country"), None)
                for country in countries:
                    self.country_combo.addItem(country.name, country.id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading countries: {str(e)}")

    def _save(self):
        name = self.name_input.text().strip()
        country_id = self.country_combo.currentData()

        try:
            with get_db() as db:
                service = BrokerService(db)

                if self.is_edit_mode:
                    update_data = BrokerUpdate(name=name, country_id=country_id)
                    service.update(self.broker_id, update_data)
                else:
                    create_data = BrokerCreate(name=name, country_id=country_id)
                    service.create(create_data)

                self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
