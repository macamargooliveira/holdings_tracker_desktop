from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QDialog
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_ticker_history_service import AssetTickerHistoryService
from holdings_tracker_desktop.ui.formatters import format_date
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class AssetTickerHistoriesWidget(EntityManagerWidget):
    def __init__(self, asset_id: int, parent=None):
        super().__init__(parent)
        self.asset_id = asset_id
        self.window().widgets_with_translation.append(self)

    def load_data(self):
        try:
            with get_db() as db:
                service = AssetTickerHistoryService(db)
                self.ui_data = service.list_all_for_ui(asset_id=self.asset_id)

        except Exception as e:
            self.show_error(f"Error loading asset ticker histories: {str(e)}")
            self.table.setRowCount(0)

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("asset_ticker_history"))
        self._populate_table(self.ui_data)

    def get_enabled_actions(self):
        return ("add", "delete")

    def get_extra_buttons(self):
        return [("back", "fa5s.arrow-left", self.on_back_clicked)]

    def on_back_clicked(self):
        from holdings_tracker_desktop.ui.widgets.assets_widget import AssetsWidget
        self.navigate_to(AssetsWidget)

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.asset_ticker_history_form import AssetTickerHistoryForm

        form = AssetTickerHistoryForm(
            asset_id=self.asset_id,
            parent=self
        )

        if form.exec() == QDialog.Accepted:
            self.load_data()

    def delete_record(self, selected_id):
        try:
            with get_db() as db:
                service = AssetTickerHistoryService(db)

                if not self.ask_confirmation(title=t('delete_asset_ticker_history'), message=t('confirm_delete')):
                    return

                deleted = service.delete(selected_id)

                if deleted:
                    self.load_data()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting asset ticker history: {str(e)}")

    def _populate_table(self, items):
        self.table.clear()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            [t("asset"), t("change_date"), t("old_ticker"), t("new_ticker")]
        )
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            ticker_item = QTableWidgetItem(item['asset_ticker'])
            ticker_item.setData(Qt.UserRole, item['id'])
            ticker_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, ticker_item)

            item_date = QTableWidgetItem(format_date(item['change_date']))
            item_date.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item_date)

            self.table.setItem(row, 2, QTableWidgetItem(item['old_ticker']))

            self.table.setItem(row, 3, QTableWidgetItem(item['new_ticker']))
