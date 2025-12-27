from PySide6.QtWidgets import QWidget, QVBoxLayout, QMenuBar, QFrame
from datetime import date as Date
from holdings_tracker_desktop.ui.global_signals import global_signals
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_type_service import AssetTypeService
from holdings_tracker_desktop.services.position_snapshot_service import PositionSnapshotService

MENU_CONFIG = {
    "asset_type": "_load_asset_types",
    "year": "_load_years"
}

class ChartsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_state()
        self._setup_ui()
        self.translate_ui()

        global_signals.asset_types_updated.connect(self.refresh_asset_types_menu)
        global_signals.broker_notes_updated.connect(self.refresh_years_menu)

    def translate_ui(self):
        for menu_name, _ in MENU_CONFIG.items():
            self.menus[menu_name].setTitle(t(menu_name))

        if self.all_asset_types_action:
            self.all_asset_types_action.setText(t('all'))

    def refresh_asset_types_menu(self):
        menu = self.menus.get("asset_type")
        if menu:
            menu.clear()
            self._load_asset_types(menu)

    def refresh_years_menu(self):
        menu = self.menus.get("year")
        if menu:
            menu.clear()
            self._load_years(menu)

    def _init_state(self):
        self.window().widgets_with_translation.append(self)
        self.menus = {}
        self.all_asset_types_action = None

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self._setup_menu(layout)
        self._setup_body_frame(layout)

    def _setup_menu(self, layout):
        menu_bar = QMenuBar(self)

        for menu_name, load_func in MENU_CONFIG.items():
            menu = menu_bar.addMenu("")
            self.menus[menu_name] = menu

            load_func = getattr(self, load_func, None)
            if callable(load_func):
                load_func(menu)

        layout.addWidget(menu_bar, stretch=0)

    def _setup_body_frame(self, layout):
        body_frame = QFrame()
        body_frame.setObjectName("BodyFrame")

        layout.addWidget(body_frame, stretch=1)

    def _load_asset_types(self, menu):
        self.all_asset_types_action = menu.addAction(t('all'))
        self.all_asset_types_action.setData(0)
        self.all_asset_types_action.triggered.connect(
            lambda _, a=self.all_asset_types_action: self._on_asset_type_selected(a.data())
        )

        with get_db() as db:
            service = AssetTypeService(db)
            for asset_type in service.list_all_models():
                action = menu.addAction(asset_type.name)
                action.setData(asset_type.id)
                action.triggered.connect(
                    lambda _, a=action: self._on_asset_type_selected(a.data())
                )

    def _on_asset_type_selected(self, asset_type_id: int):
        print(f"Asset type selected: {asset_type_id}")

    def _load_years(self, menu):
        with get_db() as db:
            service = PositionSnapshotService(db)
            min_date = service.get_earliest_snapshot_date()

            current_year = Date.today().year
            start_year = min_date.year if min_date else current_year

            for y in range(current_year, start_year - 1, -1):
                action = menu.addAction(str(y))
                action.triggered.connect(
                    lambda _, year=y: self._on_year_selected(year)
                )

    def _on_year_selected(self, year: int):
        print(f"Year selected: {year}")
