from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.core.formatters import format_datetime
from holdings_tracker_desktop.ui.dialogs.base_details_dialog import BaseDetailsDialog

class AssetTypeDetailsDialog(BaseDetailsDialog):
    def __init__(self, asset_type_id: int, parent=None):
        self.asset_type_id = asset_type_id
        super().__init__(parent)

        self._load_data()
        self.setWindowTitle(t("asset_type_details"))

    def _load_data(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.asset_type_service import AssetTypeService

        with get_db() as db:
            service = AssetTypeService(db)
            type = service.get_details(self.asset_type_id)

            self.add_detail(t("name"), type.name)
            self.add_detail(t("country"), type.country.name)
            self.add_detail(t("assets"), str(type.assets_count))
            self.add_detail(t("asset_sectors"), str(type.sectors_count))
            self.add_detail(t("created_at"), format_datetime(type.created_at_local))
            self.add_detail(t("updated_at"), format_datetime(type.updated_at_local))
