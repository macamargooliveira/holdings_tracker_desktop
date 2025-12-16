from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, 
    QDialogButtonBox, QVBoxLayout, QMessageBox
)
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.country_service import CountryService
from holdings_tracker_desktop.schemas.country import CountryCreate, CountryUpdate
from holdings_tracker_desktop.ui.translations import t

class CountryForm(QDialog):
    def __init__(self, country_id=None, initial_data=None, parent=None):
        super().__init__(parent)
        self._init_state(country_id, initial_data)
        self._setup_ui()
        self._load_initial_data()
        self.setWindowTitle(
            t("edit_country") if self.is_edit_mode else t("new_country")
        )

    def _init_state(self, country_id, initial_data):
        self.country_id = country_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = country_id is not None

    def _setup_ui(self):
        self.setMinimumWidth(350)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        form_layout.addRow(f"{t('name')}:", self.name_input)

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

    def _save(self):
        name = self.name_input.text().strip()

        try:
            with get_db() as db:
                service = CountryService(db)

                if self.is_edit_mode:
                    update_data = CountryUpdate(name=name)
                    service.update(self.country_id, update_data)
                else:
                    create_data = CountryCreate(name=name)
                    service.create(create_data)

                self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
