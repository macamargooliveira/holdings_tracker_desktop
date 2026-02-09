from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.core.formatters import format_datetime
from holdings_tracker_desktop.ui.dialogs.base_details_dialog import BaseDetailsDialog

class CurrencyDetailsDialog(BaseDetailsDialog):
    def __init__(self, currency_id: int, parent=None):
        self.currency_id = currency_id
        super().__init__(parent)

        self._load_data()
        self.setWindowTitle(t("currency_details"))

    def _load_data(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.currency_service import CurrencyService

        with get_db() as db:
            service = CurrencyService(db)
            currency = service.get_details(self.currency_id)

            self.add_detail(t("code"), currency.code)
            self.add_detail(t("name"), currency.name)
            self.add_detail(t("symbol"), currency.symbol)
            self.add_detail(t("assets"), str(currency.assets_count))
            self.add_detail(t("created_at"), format_datetime(currency.created_at_local))
            self.add_detail(t("updated_at"), format_datetime(currency.updated_at_local))
