from PySide6.QtWidgets import QDialog

from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_sector_service import AssetSectorService
from holdings_tracker_desktop.ui.core import t
from holdings_tracker_desktop.ui.core.ui_helpers import prepare_table, table_item
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class AssetSectorsWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_data(self):
        try:
            with get_db() as db:
                service = AssetSectorService(db)
                ui_data = service.list_all_for_ui()
                self._populate_table(ui_data)

        except Exception as e:
            self.show_error(f"Error loading asset sectors: {str(e)}")
            self.table.setRowCount(0)

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_widget.setText(t("asset_sectors"))
        self.table.setHorizontalHeaderLabels([t("name"), t("asset_type"), t("assets")])

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.asset_sector_form import AssetSectorForm

        form = AssetSectorForm(parent=self)

        if form.exec() == QDialog.Accepted:
            self.load_data()

    def open_edit_form(self, selected_id):
        from holdings_tracker_desktop.ui.forms.asset_sector_form import AssetSectorForm

        try:
            with get_db() as db:
                service = AssetSectorService(db)
                asset_sector = service.get(selected_id)

                form = AssetSectorForm(
                    asset_sector_id=selected_id,
                    initial_data={
                        'name': asset_sector.name,
                        'asset_type_id': asset_sector.asset_type_id
                    },
                    parent=self
                )

                if form.exec() == QDialog.Accepted:
                    self.load_data()

        except Exception as e:
            self.show_error(f"Error opening edit form: {str(e)}")

    def delete_record(self, selected_id):
        try:
            with get_db() as db:
                service = AssetSectorService(db)

                if not self.ask_confirmation(title=t('delete_asset_sector'), message=t('confirm_delete')):
                    return

                deleted = service.delete(selected_id)

                if deleted:
                    self.load_data()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting asset sector: {str(e)}")

    def _populate_table(self, items):
        prepare_table(self.table, 3, len(items))

        for row, item in enumerate(items):
            self.table.setItem(row, 0, table_item(item['name'], item['id']))
            self.table.setItem(row, 1, table_item(item['asset_type_name']))
            self.table.setItem(row, 2, table_item(str(item['assets_count'])))
