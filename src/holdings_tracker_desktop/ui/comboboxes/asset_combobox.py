from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox

class AssetComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_asset", parent)
        self.reload()

    def reload(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.asset_service import AssetService

        self._setup_placeholder()

        with get_db() as db:
            service = AssetService(db)
            for asset in service.list_all_models():
                self.addItem(asset.ticker, asset.id)
