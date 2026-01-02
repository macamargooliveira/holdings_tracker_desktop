from PySide6.QtWidgets import QDialog
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_service import AssetService
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.ui_helpers import prepare_table, table_item
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class AssetsWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window().widgets_with_translation.append(self)

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
        return [
            ("position", "fa5s.chart-line", self.on_position_clicked),
            ("ticker_change", "fa5s.history", self.on_ticker_change_clicked)
        ]

    def on_position_clicked(self):
        asset_id = self.get_selected_id()
        if not asset_id:
            return

        from holdings_tracker_desktop.ui.widgets.position_snapshots_widget import PositionSnapshotsWidget
        self.navigate_to(PositionSnapshotsWidget, asset_id)

    def on_ticker_change_clicked(self):
        asset_id = self.get_selected_id()
        if not asset_id:
            return

        from holdings_tracker_desktop.ui.widgets.asset_ticker_histories_widget import AssetTickerHistoriesWidget
        self.navigate_to(AssetTickerHistoriesWidget, asset_id)

    def _populate_table(self, items):
        prepare_table(self.table, 6, len(items))

        for row, item in enumerate(items):
            self.table.setItem(row, 0, table_item(item['ticker'], item['id']))
            self.table.setItem(row, 1, table_item(item['type_name']))
            self.table.setItem(row, 2, table_item(item['currency_code']))
            self.table.setItem(row, 3, table_item(item['sector_name']))
            self.table.setItem(row, 4, table_item(str(item['broker_notes_count'])))
            self.table.setItem(row, 5, table_item(str(item['events_count'])))
