from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.position_snapshot_service import PositionSnapshotService
from holdings_tracker_desktop.ui.comboboxes import PositionSnapshotYearComboBox
from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.core.formatters import format_date
from holdings_tracker_desktop.ui.core.ui_helpers import prepare_table, table_item, decimal_table_item
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class PositionSnapshotsWidget(EntityManagerWidget):
    def __init__(self, asset_id: int | None = None, parent=None):
        self.asset_id = asset_id
        self.year = None

        if self.asset_id is None:
            self.year_filter = PositionSnapshotYearComboBox()
            self.year_filter.currentIndexChanged.connect(self.load_data)
        else:
            self.year_filter = None

        super().__init__(parent)

    def get_toolbar_filters(self):
        return [self.year_filter] if self.year_filter else []

    def load_data(self):
        self.ui_data = []

        try:
            with get_db() as db:
                service = PositionSnapshotService(db)

                if self.asset_id:
                    self.ui_data = service.list_all_for_ui_by_asset(self.asset_id)
                else:
                    self.year = self.year_filter.currentData()
                    if self.year is not None:
                        self.ui_data = service.list_all_for_ui_by_year(self.year)

        except Exception as e:
            self.show_error(f"Error loading position snapshots: {str(e)}")

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()

        if self.year:
            self.title_widget.setText(f"{t('position')} — {self.year}")
        else:
            self.title_widget.setText(t("position"))

        if self.year_filter:
            self.year_filter.translate_placeholder()

        self._populate_table(self.ui_data)

    def get_enabled_actions(self):
        return ()

    def get_extra_buttons(self):
        return [("back", "fa5s.arrow-left", self.on_back_clicked)] if self.asset_id else []

    def on_back_clicked(self):
        from holdings_tracker_desktop.ui.widgets.assets_widget import AssetsWidget
        self.navigate_to(AssetsWidget)

    def _populate_table(self, items):
        if self.asset_id is not None:
            self._populate_table_single_asset(items)
        else:
            self._populate_table_all_assets(items)

    def _populate_table_single_asset(self, items):
        prepare_table(self.table, 6, len(items))
        self.table.setHorizontalHeaderLabels(
            [t("asset"), t("date"), t("quantity_abbr"), t("avg_price"), t("total_cost"), t("origin")]
        )

        for row, item in enumerate(items):
            self.table.setItem(row, 0, table_item(item['asset_ticker'], item['id']))
            self.table.setItem(row, 1, table_item(format_date(item['snapshot_date'])))
            self.table.setItem(row, 2, decimal_table_item(item['quantity'], 0))
            currency = item.get("asset_currency", "")
            self.table.setItem(row, 3, decimal_table_item(item['avg_price'], 2, currency))
            self.table.setItem(row, 4, decimal_table_item(item['total_cost'], 2, currency))
            self.table.setItem(row, 5, table_item(t(item['origin_action'])))

    def _populate_table_all_assets(self, items):
        prepare_table(self.table, 4, len(items))
        self.table.setHorizontalHeaderLabels(
            [t("asset"), t("quantity_abbr"), t("avg_price"), t("total_cost")]
        )

        for row, item in enumerate(items):
            self.table.setItem(row, 0, table_item(item['asset_ticker'], item['id']))
            self.table.setItem(row, 1, decimal_table_item(item['quantity'], 0))
            currency = item.get("asset_currency", "")
            self.table.setItem(row, 2, decimal_table_item(item['avg_price'], 2, currency))
            self.table.setItem(row, 3, decimal_table_item(item['total_cost'], 2, currency))
