from PySide6.QtWidgets import QWidget, QVBoxLayout, QMenuBar, QFrame, QLabel
from holdings_tracker_desktop.ui.translations import t

MENU_CONFIG = [
    "asset_types",
    "year"
]

class ChartsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_state()
        self._setup_ui()
        self.translate_ui()

    def translate_ui(self):
        for menu_name in MENU_CONFIG:
            self.menus[menu_name].setTitle(t(menu_name))

    def _init_state(self):
        self.window().widgets_with_translation.append(self)
        self.menus = {}

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self._setup_menu(layout)
        self._setup_body_frame(layout)

    def _setup_menu(self, layout):
        menu_bar = QMenuBar(self)

        for menu_name in MENU_CONFIG:
            menu = menu_bar.addMenu("")
            self.menus[menu_name] = menu

        layout.addWidget(menu_bar, stretch=0)

    def _setup_body_frame(self, layout):
        body_frame = QFrame()
        body_frame.setObjectName("BodyFrame")

        layout.addWidget(body_frame, stretch=1)
