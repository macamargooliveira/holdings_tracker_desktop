from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox

class AssetSectorComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_sector", parent)
        self.reload()

    def reload(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.asset_sector_service import AssetSectorService

        self._setup_placeholder()

        with get_db() as db:
            service = AssetSectorService(db)
            for sector in service.list_all_models():
                self.addItem(sector.name, sector.id)
