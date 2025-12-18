from PySide6.QtGui import Qt
from PySide6.QtWidgets import QTableWidgetItem, QDialog
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.broker_service import BrokerService
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.operations.entity_manager_widget import EntityManagerWidget

class BrokersWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window().widgets_with_translation.append(self)
        self.load_data()

    def load_data(self):
        try:
            with get_db() as db:
                service = BrokerService(db)
                ui_data = service.list_all_for_ui()
                self._populate_table(ui_data)

        except Exception as e:
            self.show_error(f"Error loading brokers: {str(e)}")
            self.table.setRowCount(0)

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("brokers"))
        self.table.setHorizontalHeaderLabels([t("name"), t("country"), t("broker_notes")])

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.broker_form import BrokerForm

        form = BrokerForm(parent=self)

        if form.exec() == QDialog.Accepted:
            self.load_data()

    def open_edit_form(self, selected_id):
        from holdings_tracker_desktop.ui.forms.broker_form import BrokerForm

        try:
            with get_db() as db:
                service = BrokerService(db)
                broker = service.get(selected_id)

                form = BrokerForm(
                    broker_id=selected_id,
                    initial_data={
                        'name': broker.name,
                        'country_id': broker.country_id
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
                service = BrokerService(db)

                if not self.ask_confirmation(title=t('delete_broker'), message=t('confirm_delete')):
                    return

                deleted = service.delete(selected_id)

                if deleted:
                    self.load_data()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting broker: {str(e)}")

    def _populate_table(self, items):
        self.table.clear()
        self.table.setColumnCount(3)
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            name_item = QTableWidgetItem(item['name'])
            name_item.setData(Qt.UserRole, item['id'])
            self.table.setItem(row, 0, name_item)

            self.table.setItem(row, 1, QTableWidgetItem(item['country_name']))

            count_item = QTableWidgetItem(str(item['broker_notes_count']))
            count_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, count_item)
