from PySide6.QtWidgets import QDialog
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_type_service import AssetTypeService
from holdings_tracker_desktop.ui.global_signals import global_signals
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.ui_helpers import prepare_table, table_item
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class AssetTypesWidget(EntityManagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window().widgets_with_translation.append(self)

    def load_data(self):
        try:
            with get_db() as db:
                service = AssetTypeService(db)
                ui_data = service.list_all_for_ui()
                self._populate_table(ui_data)

        except Exception as e:
            self.show_error(f"Error loading asset types: {str(e)}")
            self.table.setRowCount(0)

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("asset_types"))
        self.table.setHorizontalHeaderLabels([t("name"), t("country"), t("assets"), t("asset_sectors")])

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.asset_type_form import AssetTypeForm

        form = AssetTypeForm(parent=self)

        if form.exec() == QDialog.Accepted:
            self.load_data()
            global_signals.asset_types_updated.emit()

    def open_edit_form(self, selected_id):
        from holdings_tracker_desktop.ui.forms.asset_type_form import AssetTypeForm

        try:
            with get_db() as db:
                service = AssetTypeService(db)
                asset_type = service.get(selected_id)

                form = AssetTypeForm(
                    asset_type_id=selected_id,
                    initial_data={
                        'name': asset_type.name,
                        'country_id': asset_type.country_id
                    },
                    parent=self
                )

                if form.exec() == QDialog.Accepted:
                    self.load_data()
                    global_signals.asset_types_updated.emit()

        except Exception as e:
            self.show_error(f"Error opening edit form: {str(e)}")

    def delete_record(self, selected_id):
        try:
            with get_db() as db:
                service = AssetTypeService(db)

                if not self.ask_confirmation(title=t('delete_asset_type'), message=t('confirm_delete')):
                    return

                deleted = service.delete(selected_id)

                if deleted:
                    self.load_data()
                    global_signals.asset_types_updated.emit()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting asset type: {str(e)}")

    def _populate_table(self, items):
        prepare_table(self.table, 4, len(items))

        for row, item in enumerate(items):
            self.table.setItem(row, 0, table_item(item['name'], item['id']))
            self.table.setItem(row, 1, table_item(item['country_name'], None))
            self.table.setItem(row, 2, table_item(str(item['assets_count'])))
            self.table.setItem(row, 3, table_item(str(item['sectors_count'])))
