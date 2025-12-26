from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem
from decimal import Decimal
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.position_snapshot_service import PositionSnapshotService
from holdings_tracker_desktop.ui.formatters import format_date, format_decimal
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class PositionSnapshotsWidget(EntityManagerWidget):
    def __init__(self, asset_id: int, parent=None):
        super().__init__(parent)
        self.asset_id = asset_id
        self.window().widgets_with_translation.append(self)
        self.load_data()

    def load_data(self):
        try:
            with get_db() as db:
                service = PositionSnapshotService(db)
                self.ui_data = service.list_all_for_ui(asset_id=self.asset_id)

        except Exception as e:
            self.show_error(f"Error loading position snapshots: {str(e)}")

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("position"))
        self._populate_table(self.ui_data)

    def get_enabled_actions(self):
        return ()

    def get_extra_buttons(self):
        return [("back", "fa5s.arrow-left", self.on_back_clicked)]

    def on_back_clicked(self):
        from holdings_tracker_desktop.ui.widgets.assets_widget import AssetsWidget
        self.navigate_to(AssetsWidget)

    def _populate_table(self, items):
        self.table.clear()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [t("asset"), t("date"), t("quantity_abbr"), t("avg_price"), t("total_cost")]
        )
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            ticker_item = QTableWidgetItem(item['asset_ticker'])
            ticker_item.setData(Qt.UserRole, item['id'])
            ticker_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, ticker_item)

            item_date = QTableWidgetItem(format_date(item['snapshot_date']))
            item_date.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item_date)

            currency = item.get("asset_currency", "")
            self.table.setItem(row, 2, self._decimal_item(item['quantity'], 0))
            self.table.setItem(row, 3, self._decimal_item(item['avg_price'], 2, currency))
            self.table.setItem(row, 4, self._decimal_item(item['total_cost'], 2, currency))

    def _decimal_item(
            self, 
            value: Decimal, 
            decimals: int = 2,
            currency: str = ""
        ) -> QTableWidgetItem:
        text = format_decimal(value, decimals)
        text = f"{currency} {text}"
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        return item
