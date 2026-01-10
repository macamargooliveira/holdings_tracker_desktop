from holdings_tracker_desktop.ui.comboboxes.base_combobox import BaseComboBox
from holdings_tracker_desktop.ui.translations import t

class EventTypeComboBox(BaseComboBox):
    def __init__(self, parent=None):
        super().__init__("select_event_type", parent)
        self.reload()

    def reload(self):
        from holdings_tracker_desktop.models.asset_event import AssetEventType

        self._setup_placeholder()

        for event_type in AssetEventType:
            self.addItem(t(event_type.value.lower()), event_type)
