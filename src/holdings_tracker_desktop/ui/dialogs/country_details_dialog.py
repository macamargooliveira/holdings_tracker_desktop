from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.core.formatters import format_datetime
from holdings_tracker_desktop.ui.dialogs.base_details_dialog import BaseDetailsDialog

class CountryDetailsDialog(BaseDetailsDialog):
    def __init__(self, country_id: int, parent=None):
        self.country_id = country_id
        super().__init__(parent)

        self._load_data()
        self.setWindowTitle(t("country_details"))

    def _load_data(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.country_service import CountryService

        with get_db() as db:
            service = CountryService(db)
            country = service.get_details(self.country_id)

            self.add_detail(t("name"), country.name)
            self.add_detail(t("asset_types"), str(country.asset_types_count))
            self.add_detail(t("brokers"), str(country.brokers_count))
            self.add_detail(t("created_at"), format_datetime(country.created_at_local))
            self.add_detail(t("updated_at"), format_datetime(country.updated_at_local))
