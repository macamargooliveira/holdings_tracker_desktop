from PySide6.QtWidgets import QTableWidgetItem, QDialog
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.models.asset_event import AssetEventType
from holdings_tracker_desktop.services.asset_event_service import AssetEventService
from holdings_tracker_desktop.ui.formatters import format_date
from holdings_tracker_desktop.ui.global_signals import global_signals
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.ui_helpers import prepare_table, table_item
from holdings_tracker_desktop.ui.widgets.entity_manager_widget import EntityManagerWidget

class AssetEventsWidget(EntityManagerWidget):
    def __init__(self, asset_id: int, parent=None):
        super().__init__(parent)
        self.asset_id = asset_id
        self.window().widgets_with_translation.append(self)

    def load_data(self):
        try:
            with get_db() as db:
                service = AssetEventService(db)
                ui_data = service.list_all_for_ui(asset_id=self.asset_id)
                self._populate_table(ui_data)

        except Exception as e:
            self.show_error(f"Error loading asset events: {str(e)}")
            self.table.setRowCount(0)

        self.translate_ui()

    def translate_ui(self):
        super().translate_ui()
        self.title_label.setText(t("events"))
        self.table.setHorizontalHeaderLabels([t("asset"), t("date"), t("type")])

    def get_extra_buttons(self):
        return [("back", "fa5s.arrow-left", self.on_back_clicked)]

    def on_back_clicked(self):
        from holdings_tracker_desktop.ui.widgets.assets_widget import AssetsWidget
        self.navigate_to(AssetsWidget)

    def open_new_form(self):
        from holdings_tracker_desktop.ui.forms.asset_event_form import AssetEventForm

        form = AssetEventForm(
            asset_id=self.asset_id,
            parent=self
        )

        if form.exec() == QDialog.Accepted:
            self.load_data()
            global_signals.asset_events_updated.emit()

    def open_edit_form(self, selected_id):
        from holdings_tracker_desktop.ui.forms.asset_event_form import AssetEventForm

        try:
            with get_db() as db:
                service = AssetEventService(db)
                asset_event = service.get(selected_id)

                form = AssetEventForm(
                    asset_event_id=selected_id,
                    asset_id=self.asset_id,
                    initial_data={
                        'date': asset_event.date,
                        'event_type': asset_event.event_type,
                        'factor': asset_event.factor,
                        'quantity': asset_event.quantity,
                        'price': asset_event.price,
                        'converted_to_asset_id': asset_event.converted_to_asset_id,
                        'conversion_quantity': asset_event.conversion_quantity,
                        'residual_value': asset_event.residual_value,
                    },
                    parent=self
                )

                if form.exec() == QDialog.Accepted:
                    self.load_data()
                    global_signals.asset_events_updated.emit()

        except Exception as e:
            self.show_error(f"Error opening edit form: {str(e)}")

    def delete_record(self, selected_id):
        try:
            with get_db() as db:
                service = AssetEventService(db)

                if not self.ask_confirmation(title=t('delete_asset_event'), message=t('confirm_delete')):
                    return

                deleted = service.delete(selected_id)

                if deleted:
                    self.load_data()
                    global_signals.asset_events_updated.emit()
                else:
                    self.show_error(f"Delete failed")

        except Exception as e:
            self.show_error(f"Error deleting asset event: {str(e)}")

    def _populate_table(self, items):
        prepare_table(self.table, 3, len(items))

        for row, item in enumerate(items):
            self.table.setItem(row, 0, table_item(item['asset_ticker'], item['id']))
            self.table.setItem(row, 1, table_item(format_date(item['date'])))
            self.table.setItem(row, 2, self._event_type_item(item['event_type']))

    def _event_type_item(self, event_type: AssetEventType) -> QTableWidgetItem:
        label_map = {
            AssetEventType.SPLIT: t("split"),
            AssetEventType.REVERSE_SPLIT: t("reverse_split"),
            AssetEventType.AMORTIZATION: t("amortization"),
            AssetEventType.SUBSCRIPTION: t("subscription"),
            AssetEventType.CONVERSION: t("conversion"),
        }

        text = label_map.get(event_type, str(event_type))
        return table_item(text)
