from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.core.formatters import format_datetime
from holdings_tracker_desktop.ui.dialogs.base_details_dialog import BaseDetailsDialog

class BrokerDetailsDialog(BaseDetailsDialog):
    def __init__(self, broker_id: int, parent=None):
        self.broker_id = broker_id
        super().__init__(parent)

        self._load_data()
        self.setWindowTitle(t("broker_details"))

    def _load_data(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.broker_service import BrokerService

        with get_db() as db:
            service = BrokerService(db)
            broker = service.get_details(self.broker_id)

            self.add_detail(t("name"), broker.name)
            self.add_detail(t("country"), broker.country.name)
            self.add_detail(t("broker_notes"), str(broker.broker_notes_count))
            self.add_detail(t("created_at"), format_datetime(broker.created_at_local))
            self.add_detail(t("updated_at"), format_datetime(broker.updated_at_local))
