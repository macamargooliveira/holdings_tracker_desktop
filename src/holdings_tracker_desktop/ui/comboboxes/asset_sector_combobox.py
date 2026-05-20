from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox

class AssetSectorComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_sector", parent, searchable=True)
        self.reload()

    def reload(self):
        self.load_for_type(None)

    def load_for_type(self, type_id):
        """Load sectors filtered by asset type. If `type_id` is None, load all."""
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.asset_sector_service import AssetSectorService

        self._setup_placeholder()

        with get_db() as db:
            service = AssetSectorService(db)
            sectors = []
            if type_id is None:
                for sector in service.list_all_models():
                    sectors.append(sector)
            else:
                for sector in service.get_by_asset_type(type_id):
                    sectors.append(sector)

            for sector in sectors:
                self.addItem(sector.name, sector.id)
