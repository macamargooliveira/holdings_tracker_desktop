from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.core.formatters import format_date, format_datetime
from holdings_tracker_desktop.ui.dialogs.base_details_dialog import BaseDetailsDialog

class TickerHistoryDetailsDialog(BaseDetailsDialog):
    def __init__(self, asset_ticker_history_id: int, parent=None):
        self.asset_ticker_history_id = asset_ticker_history_id
        super().__init__(parent)

        self._load_data()
        self.setWindowTitle(t("ticker_history_details"))

    def _load_data(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.asset_ticker_history_service import (
            AssetTickerHistoryService
        )

        with get_db() as db:
            service = AssetTickerHistoryService(db)
            history = service.get_details(self.asset_ticker_history_id)

            self.add_detail(t("asset"), history.asset.ticker)
            self.add_detail(t("change_date"), format_date(history.change_date))
            self.add_detail(t("old_ticker"), history.old_ticker)
            self.add_detail(t("new_ticker"), history.new_ticker)
            self.add_detail(t("created_at"), format_datetime(history.created_at_local))
            self.add_detail(t("updated_at"), format_datetime(history.updated_at_local))
