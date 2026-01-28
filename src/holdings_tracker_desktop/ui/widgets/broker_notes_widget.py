from PySide6.QtWidgets import QTableWidgetItem, QDialog

from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.models.broker_note import OperationType
from holdings_tracker_desktop.services.broker_note_service import BrokerNoteService
from holdings_tracker_desktop.ui.core import t, global_signals
from holdings_tracker_desktop.ui.core.formatters import format_date
from holdings_tracker_desktop.ui.core.ui_helpers import prepare_table, table_item, decimal_table_item
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class BrokerNotesWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.title_widget.setText(t("broker_notes"))
        self._populate_table(self.ui_data)

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.broker_note_form import BrokerNoteForm

        form = BrokerNoteForm(parent=self)

        if form.exec() == QDialog.Accepted:
            self.load_data()
            global_signals.broker_notes_updated.emit()

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
                    global_signals.broker_notes_updated.emit()

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
                    global_signals.broker_notes_updated.emit()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting broker note: {str(e)}")

    def _populate_table(self, items):
        prepare_table(self.table, 8, len(items))

        self.table.setHorizontalHeaderLabels(
            [t("date"), t("operation_abbr"), t("asset"), t("quantity_abbr"), 
             t("price"), t("fees"), t("taxes"), t("total_value")]
        )

        for row, item in enumerate(items):
            self.table.setItem(row, 0, table_item(format_date(item['date']), item['id']))
            self.table.setItem(row, 1, self._operation_item(item['operation']))
            self.table.setItem(row, 2, table_item(item['asset_ticker']))
            self.table.setItem(row, 3, decimal_table_item(item['quantity'], 0))
            currency = item.get("asset_currency", "")
            self.table.setItem(row, 4, decimal_table_item(item['price'], 2, currency))
            self.table.setItem(row, 5, decimal_table_item(item['fees'], 2, currency))
            self.table.setItem(row, 6, decimal_table_item(item['taxes'], 2, currency))
            self.table.setItem(row, 7, decimal_table_item(item['total_value'], 2, currency))

    def _operation_item(self, operation: OperationType) -> QTableWidgetItem:
        label_map = {
            OperationType.BUY: t("buy"),
            OperationType.SELL: t("sell"),
        }

        text = label_map.get(operation, str(operation))
        return table_item(text)
