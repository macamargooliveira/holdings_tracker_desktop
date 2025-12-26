from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QDialog
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_service import AssetService
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class AssetsWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window().widgets_with_translation.append(self)
        self.load_data()

    def load_data(self):
        try:
            with get_db() as db:
                service = AssetService(db)
                ui_data = service.list_all_for_ui()
                self._populate_table(ui_data)

        except Exception as e:
            self.show_error(f"Error loading assets: {str(e)}")
            self.table.setRowCount(0)

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("assets"))
        self.table.setHorizontalHeaderLabels(
            [t("ticker"), t("type"), t("currency"), t("sector"), t("notes"), t("events")]
        )

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.asset_form import AssetForm

        form = AssetForm(parent=self)

        if form.exec() == QDialog.Accepted:
            self.load_data()

    def open_edit_form(self, selected_id):
        from holdings_tracker_desktop.ui.forms.asset_form import AssetForm

        try:
            with get_db() as db:
                service = AssetService(db)
                asset = service.get(selected_id)

                form = AssetForm(
                    asset_id=selected_id,
                    initial_data={
                        'ticker': asset.ticker,
                        'type_id': asset.type_id,
                        'currency_id': asset.currency_id,
                        'sector_id': asset.sector_id
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
                service = AssetService(db)

                if not self.ask_confirmation(title=t('delete_asset'), message=t('confirm_delete')):
                    return

                deleted = service.delete(selected_id)

                if deleted:
                    self.load_data()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting asset: {str(e)}")

    def get_extra_buttons(self):
        return [("position", "fa5s.chart-line", self.on_position_clicked)]

    def on_position_clicked(self):
        asset_id = self.get_selected_id()
        if not asset_id:
            return

        from holdings_tracker_desktop.ui.widgets.position_snapshots_widget import PositionSnapshotsWidget
        self.navigate_to(PositionSnapshotsWidget, asset_id)

    def _populate_table(self, items):
        self.table.clear()
        self.table.setColumnCount(6)
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            ticker_item = QTableWidgetItem(item['ticker'])
            ticker_item.setData(Qt.UserRole, item['id'])
            ticker_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, ticker_item)

            type_item = QTableWidgetItem(item['type_name'])
            type_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, type_item)

            currency_item = QTableWidgetItem(item['currency_code'])
            currency_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, currency_item)

            self.table.setItem(row, 3, QTableWidgetItem(item['sector_name']))

            broker_notes_count = QTableWidgetItem(str(item['broker_notes_count']))
            broker_notes_count.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, broker_notes_count)

            events_count = QTableWidgetItem(str(item['events_count']))
            events_count.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, events_count)
