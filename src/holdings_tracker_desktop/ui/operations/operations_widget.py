from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMenuBar, QSizePolicy
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.operations.assets_widget import AssetsWidget
from holdings_tracker_desktop.ui.operations.asset_sectors_widget import AssetSectorsWidget
from holdings_tracker_desktop.ui.operations.asset_types_widget import AssetTypesWidget
from holdings_tracker_desktop.ui.operations.brokers_widget import BrokersWidget
from holdings_tracker_desktop.ui.operations.broker_notes_widget import BrokerNotesWidget
from holdings_tracker_desktop.ui.operations.countries_widget import CountriesWidget
from holdings_tracker_desktop.ui.operations.currencies_widget import CurrenciesWidget
import importlib.resources as res

MENU_CONFIG = {
    "bar": [
        ("broker_notes", BrokerNotesWidget),
        ("assets", AssetsWidget),
    ],
    "basics": [
        ("asset_types", AssetTypesWidget),
        ("asset_sectors", AssetSectorsWidget),
        ("brokers", BrokersWidget),
        ("currencies", CurrenciesWidget),
        ("countries", CountriesWidget),
    ],
    "languages": [
        ("English", "en_US", "us.svg"),
        ("Português", "pt_BR", "br.svg"),
    ]
}

FLAGS_PACKAGE = "holdings_tracker_desktop.ui.flags"

class OperationsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_state(parent)
        self._setup_ui()
        self.translate_ui()

    def translate_ui(self):
        for menu_name in MENU_CONFIG:
            if menu_name != "bar":
                self.menus[menu_name].setTitle(t(menu_name))

        for menu_name, entries in MENU_CONFIG.items():
            if menu_name == "languages":
                continue

            for action_name, _ in entries:
                self.actions[action_name].setText(t(action_name))

    def show_widget(self, widget_cls):
        if widget_cls not in self.widget_cache:
            self.widget_cache[widget_cls] = widget_cls(self)

        widget = self.widget_cache[widget_cls]
        self._set_content_widget(widget)

    def _init_state(self, parent):
        self.window().widgets_with_translation.append(self)
        self.parent_window = parent
        self.actions = {}
        self.menus = {}
        self.widget_cache = {}

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._create_actions()
        self._setup_menu(layout)
        self._setup_content_area(layout)
        self.show_widget(BrokerNotesWidget)

    def _create_actions(self):
        for menu_name, entries in MENU_CONFIG.items():
            for item in entries:

                if menu_name == "languages":
                    label, lang_code, svg_icon = item
                    action = QAction(label, self)
                    action.setIcon(self._load_svg_icon(svg_icon))
                    action.triggered.connect(
                        lambda _, lang=lang_code: self.parent_window.set_language(lang)
                    )
                    self.actions[label] = action
                    continue

                action_name, widget_cls = item
                action = QAction("", self)
                action.triggered.connect(
                    lambda _, cls=widget_cls: self.show_widget(cls)
                )
                self.actions[action_name] = action

    def _load_svg_icon(self, filename: str) -> QIcon:
        with res.open_binary(FLAGS_PACKAGE, filename) as f:
            data = f.read()

        pix = QPixmap()
        pix.loadFromData(data, "SVG")
        return QIcon(pix)

    def _setup_menu(self, layout):
        menu_bar = QMenuBar(self)

        for menu_name, entries in MENU_CONFIG.items():
            if menu_name == "bar":
                for action_name, _ in entries:
                    menu_bar.addAction(self.actions[action_name])
                continue

            menu = menu_bar.addMenu("")
            self.menus[menu_name] = menu

            for item in entries:
                if menu_name == "languages":
                    label, _, _ = item
                    menu.addAction(self.actions[label])
                else:
                    action_name, _ = item
                    menu.addAction(self.actions[action_name])

        layout.addWidget(menu_bar)

    def _setup_content_area(self, layout):
        self.content_area = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.content_area.setLayout(content_layout)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.content_area)

    def _set_content_widget(self, widget: QWidget):
        layout = self.content_area.layout()

        if layout.count() > 0:
            old_widget = layout.itemAt(0).widget()
            layout.removeWidget(old_widget)
            old_widget.hide()

        layout.addWidget(widget)
        widget.show()
