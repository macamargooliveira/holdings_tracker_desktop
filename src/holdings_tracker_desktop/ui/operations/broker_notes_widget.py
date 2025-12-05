from PySide6.QtGui import Qt
from PySide6.QtWidgets import QTableWidgetItem
from sqlalchemy.orm import joinedload
from holdings_tracker_desktop.database.database import SessionLocal
from holdings_tracker_desktop.models.broker_note import BrokerNote
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.operations.entity_manager_widget import EntityManagerWidget

class BrokerNotesWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window().widgets_with_translation.append(self)
        self.load_data()

    def load_data(self):
        items = self._get_items()
        self._populate_table(items)
        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("broker_notes"))
        self.table.setHorizontalHeaderLabels(
            [t("date"), t("operation"), t("asset"), t("quantity"), 
             t("price"), t("fees"), t("taxes"), t("total_value")]
        )

    def open_new_form(self):
        print("Open AssetType NEW form")

    def open_edit_form(self, selected_id):
        print("Edit AssetType ID:", selected_id)

    def delete_record(self, selected_id):
        print("Delete AssetType ID:", selected_id)

    def _get_items(self):
        """Query database and return list of BrokerNote objects."""
        session = SessionLocal()

        try:
            items = (
                session.query(BrokerNote)
                .options(joinedload(BrokerNote.broker), joinedload(BrokerNote.asset))
                .order_by(BrokerNote.date)
                .all()
            )
        finally:
            session.close()

        return items

    def _populate_table(self, items):
        """Clears and fills the table with rows based on items."""
        self.table.clear()
        self.table.setColumnCount(8)
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            item_date = QTableWidgetItem(item.date)
            item_date.setData(Qt.UserRole, item.id)
            self.table.setItem(row, 0, item_date)
            self.table.setItem(row, 1, QTableWidgetItem(item.operation.value))
            self.table.setItem(row, 2, QTableWidgetItem(item.asset.ticker))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.quantity)))
            self.table.setItem(row, 4, QTableWidgetItem(str(item.price)))
            self.table.setItem(row, 5, QTableWidgetItem(str(item.fees)))
            self.table.setItem(row, 6, QTableWidgetItem(str(item.taxes)))
            self.table.setItem(row, 7, QTableWidgetItem(str(item.total_value))) 
