from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QDialog
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.country_service import CountryService
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class CountriesWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window().widgets_with_translation.append(self)

    def load_data(self):
        try:
            with get_db() as db:
                service = CountryService(db)
                ui_data = service.list_all_for_ui()
                self._populate_table(ui_data)

        except Exception as e:
            self.show_error(f"Error loading countries: {str(e)}")
            self.table.setRowCount(0)

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("countries"))
        self.table.setHorizontalHeaderLabels([t("name"), t("asset_types"), t("brokers")])

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.country_form import CountryForm

        form = CountryForm(parent=self)

        if form.exec() == QDialog.Accepted:
            self.load_data()

    def open_edit_form(self, selected_id):
        from holdings_tracker_desktop.ui.forms.country_form import CountryForm

        try:
            with get_db() as db:
                service = CountryService(db)
                country = service.get(selected_id)

                form = CountryForm(
                    country_id=selected_id,
                    initial_data={
                        'name': country.name
                    },
                    parent=self
                )

                if form.exec() == QDialog.Accepted:
                    self.load_data()

        except Exception as e:
            self.show_error(f"Error opening edit form: {str(e)}")

    def delete_record(self, selected_id):
        try:
            with get_db() as db:
                service = CountryService(db)

                if not self.ask_confirmation(title=t('delete_country'), message=t('confirm_delete')):
                    return

                deleted = service.delete(selected_id)

                if deleted:
                    self.load_data()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting country: {str(e)}")

    def _populate_table(self, items):
        self.table.clear()
        self.table.setColumnCount(3)
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            name_item = QTableWidgetItem(item['name'])
            name_item.setData(Qt.UserRole, item['id'])
            self.table.setItem(row, 0, name_item)

            count_asset_types_item = QTableWidgetItem(str(item['asset_types_count']))
            count_asset_types_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, count_asset_types_item)

            count_brokers_item = QTableWidgetItem(str(item['brokers_count']))
            count_brokers_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, count_brokers_item)
