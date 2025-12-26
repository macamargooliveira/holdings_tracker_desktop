from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox

class CurrencyComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_currency", parent)
        self.reload()

    def reload(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.currency_service import CurrencyService

        self._setup_placeholder()

        with get_db() as db:
            service = CurrencyService(db)
            for currency in service.list_all_models():
                self.addItem(currency.code, currency.id)
