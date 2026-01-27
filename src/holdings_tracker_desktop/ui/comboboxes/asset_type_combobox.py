from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox

class AssetTypeComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_asset_type", parent, searchable=True)
        self.reload()

    def reload(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.asset_type_service import AssetTypeService

        self._setup_placeholder()

        with get_db() as db:
            service = AssetTypeService(db)
            for asset_type in service.list_all_models():
                self.addItem(asset_type.name, asset_type.id)
