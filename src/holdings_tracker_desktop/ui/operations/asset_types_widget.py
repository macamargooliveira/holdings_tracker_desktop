from PySide6.QtGui import Qt
from PySide6.QtWidgets import QTableWidgetItem
from sqlalchemy.orm import joinedload
from holdings_tracker_desktop.database.database import SessionLocal
from holdings_tracker_desktop.models.asset_type import AssetType
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.operations.entity_manager_widget import EntityManagerWidget

class AssetTypesWidget(EntityManagerWidget):
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
        self.title_label.setText(t("asset_types"))
        self.table.setHorizontalHeaderLabels([t("name"), t("country")])

    def open_new_form(self):
        print("Open AssetType NEW form")

    def open_edit_form(self, selected_id):
        print("Edit AssetType ID:", selected_id)

    def delete_record(self, selected_id):
        print("Delete AssetType ID:", selected_id)

    def _get_items(self):
        """Query database and return list of AssetType objects."""
        session = SessionLocal()

        try:
            items = (
                session.query(AssetType)
                .options(joinedload(AssetType.country))
                .order_by(AssetType.id)
                .all()
            )
        finally:
            session.close()

        return items

    def _populate_table(self, items):
        """Clears and fills the table with rows based on items."""
        self.table.clear()
        self.table.setColumnCount(2)
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            item_name = QTableWidgetItem(item.name)
            item_name.setData(Qt.UserRole, item.id)
            self.table.setItem(row, 0, item_name)

            self.table.setItem(row, 1, QTableWidgetItem(item.country.name))
