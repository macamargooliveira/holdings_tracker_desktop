from PySide6.QtGui import Qt
from PySide6.QtWidgets import QTableWidgetItem, QDialog
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.currency_service import CurrencyService
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.operations.entity_manager_widget import EntityManagerWidget

class CurrenciesWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window().widgets_with_translation.append(self)
        self.load_data()

    def load_data(self):
        try:
            with get_db() as db:
                service = CurrencyService(db)
                ui_data = service.list_all_for_ui()
                self._populate_table(ui_data)

        except Exception as e:
            self.show_error(f"Error loading currencies: {str(e)}")
            self.table.setRowCount(0)

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("currencies"))
        self.table.setHorizontalHeaderLabels([t("code"), t("name"), t("symbol"), t("assets")])

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.currency_form import CurrencyForm

        form = CurrencyForm(parent=self)

        if form.exec() == QDialog.Accepted:
            self.load_data()

    def open_edit_form(self, selected_id):
        from holdings_tracker_desktop.ui.forms.currency_form import CurrencyForm

        try:
            with get_db() as db:
                service = CurrencyService(db)
                currency = service.get(selected_id)

                form = CurrencyForm(
                    currency_id=selected_id,
                    initial_data={
                        'code': currency.code,
                        'name': currency.name,
                        'symbol': currency.symbol,
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
                service = CurrencyService(db)

                if not self.ask_confirmation(title=t('delete_currency'), message=t('confirm_delete')):
                    return

                deleted = service.delete(selected_id)

                if deleted:
                    self.load_data()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting currency: {str(e)}")

    def _populate_table(self, items):
        self.table.clear()
        self.table.setColumnCount(4)
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            code_item = QTableWidgetItem(item['code'])
            code_item.setData(Qt.UserRole, item['id'])
            code_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, code_item)

            self.table.setItem(row, 1, QTableWidgetItem(item['name']))

            symbol_item = QTableWidgetItem(item['symbol'])
            symbol_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, symbol_item)

            count_item = QTableWidgetItem(str(item['assets_count']))
            count_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, count_item)
