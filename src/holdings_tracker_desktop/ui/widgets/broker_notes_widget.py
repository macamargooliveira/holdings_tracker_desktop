from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QDialog
from decimal import Decimal
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.models.broker_note import OperationType
from holdings_tracker_desktop.services.broker_note_service import BrokerNoteService
from holdings_tracker_desktop.ui.formatters import format_date, format_decimal
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class BrokerNotesWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window().widgets_with_translation.append(self)
        self.load_data()

    def load_data(self):
        try:
            with get_db() as db:
                service = BrokerNoteService(db)
                self.ui_data = service.list_all_for_ui()

        except Exception as e:
            self.show_error(f"Error loading broker notes: {str(e)}")

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("broker_notes"))
        self._populate_table(self.ui_data)

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.broker_note_form import BrokerNoteForm

        form = BrokerNoteForm(parent=self)

        if form.exec() == QDialog.Accepted:
            self.load_data()

    def open_edit_form(self, selected_id):
        from holdings_tracker_desktop.ui.forms.broker_note_form import BrokerNoteForm

        try:
            with get_db() as db:
                service = BrokerNoteService(db)
                broker_note = service.get(selected_id)

                form = BrokerNoteForm(
                    broker_note_id=selected_id,
                    initial_data={
                        'date': broker_note.date,
                        'operation': broker_note.operation,
                        'broker_id': broker_note.broker_id,
                        'asset_id': broker_note.asset_id,
                        'quantity': broker_note.quantity,
                        'price': broker_note.price,
                        'fees': broker_note.fees,
                        'taxes': broker_note.taxes,
                        'note_number': broker_note.note_number
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
                service = BrokerNoteService(db)

                if not self.ask_confirmation(title=t('delete_broker_note'), message=t('confirm_delete')):
                    return

                deleted = service.delete(selected_id)

                if deleted:
                    self.load_data()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting broker note: {str(e)}")

    def _populate_table(self, items):
        self.table.clear()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [t("date"), t("operation_abbr"), t("asset"), t("quantity_abbr"), 
             t("price"), t("fees"), t("taxes"), t("total_value")]
        )
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            item_date = QTableWidgetItem(format_date(item['date']))
            item_date.setData(Qt.UserRole, item['id'])
            item_date.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item_date)

            self.table.setItem(row, 1, self._operation_item(item['operation']))

            ticker_item = QTableWidgetItem(item['asset_ticker'])
            ticker_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, ticker_item)

            self.table.setItem(row, 3, self._decimal_item(item['quantity'], 0))
            self.table.setItem(row, 4, self._decimal_item(item['price'], 2))
            self.table.setItem(row, 5, self._decimal_item(item['fees'], 2))
            self.table.setItem(row, 6, self._decimal_item(item['taxes'], 2))
            self.table.setItem(row, 7, self._decimal_item(item['total_value'], 2))

    def _operation_item(self, operation: OperationType) -> QTableWidgetItem:
        label_map = {
            OperationType.BUY: t("buy"),
            OperationType.SELL: t("sell"),
        }

        text = label_map.get(operation, str(operation))
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def _decimal_item(self, value: Decimal, decimals: int = 2) -> QTableWidgetItem:
        text = format_decimal(value, decimals)
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        return item
