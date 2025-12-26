from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox

class BrokerComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_broker", parent)
        self.reload()

    def reload(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.broker_service import BrokerService

        self._setup_placeholder()

        with get_db() as db:
            service = BrokerService(db)
            for broker in service.list_all_models():
                self.addItem(broker.name, broker.id)
