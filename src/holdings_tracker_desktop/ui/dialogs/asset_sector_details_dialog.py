from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.core.formatters import format_datetime
from holdings_tracker_desktop.ui.dialogs.base_details_dialog import BaseDetailsDialog

class AssetSectorDetailsDialog(BaseDetailsDialog):
    def __init__(self, asset_sector_id: int, parent=None):
        self.asset_sector_id = asset_sector_id
        super().__init__(parent)

        self._load_data()
        self.setWindowTitle(t("asset_sector_details"))

    def _load_data(self):
        from holdings_tracker_desktop.database import get_db
        from holdings_tracker_desktop.services.asset_sector_service import AssetSectorService

        with get_db() as db:
            service = AssetSectorService(db)
            sector = service.get_details(self.asset_sector_id)

            self.add_detail(t("name"), sector.name)
            self.add_detail(t("asset_type"), sector.asset_type.name)
            self.add_detail(t("assets"), str(sector.assets_count))
            self.add_detail(t("created_at"), format_datetime(sector.created_at_local))
            self.add_detail(t("updated_at"), format_datetime(sector.updated_at_local))
