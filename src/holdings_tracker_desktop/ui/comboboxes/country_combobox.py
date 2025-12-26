from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox

class CountryComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_country", parent)
        self.reload()

    def reload(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.country_service import CountryService

        self._setup_placeholder()

        with get_db() as db:
            service = CountryService(db)
            for country in service.list_all_models():
                self.addItem(country.name, country.id)
