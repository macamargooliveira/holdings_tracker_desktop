from dataclasses import dataclass
from datetime import date as Date
from typing import Optional

from PySide6.QtWidgets import QVBoxLayout, QMenuBar

from holdings_tracker_desktop.database import get_db
from holdings_tracker_desktop.services.asset_type_service import AssetTypeService
from holdings_tracker_desktop.services.position_snapshot_service import PositionSnapshotService
from holdings_tracker_desktop.ui.core import t, global_signals
from holdings_tracker_desktop.ui.widgets.pie_chart_widget import PieChartWidget
from holdings_tracker_desktop.ui.widgets.translatable_widget import TranslatableWidget

MENU_KEYS = ("charts", "asset_type", "year")

TRANSLATABLE_ACTIONS = ("by_assets", "by_sectors", "all")

@dataclass
class ChartState:
    dimension: str = "asset"
    asset_type_id: Optional[int] = None
    year: int = Date.today().year

class ChartsWidget(TranslatableWidget):

    CHART_LOADERS = {
        "asset": PositionSnapshotService.get_allocation_by_asset,
        "sector": PositionSnapshotService.get_allocation_by_sector
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_state()
        self._setup_ui()
        self.translate_ui()

        global_signals.asset_types_updated.connect(self.refresh_asset_types_menu)
        global_signals.asset_events_updated.connect(self.refresh_years_menu)
        global_signals.broker_notes_updated.connect(self.refresh_years_menu)

    def translate_ui(self):
        for menu_name in MENU_KEYS:
            self.menus[menu_name].setTitle(t(menu_name))

        for key in TRANSLATABLE_ACTIONS:
            action = self.actions.get(key)
            if action:
                action.setText(t(key))

        self._refresh_chart()

    def refresh_asset_types_menu(self):
        menu = self.menus.get("asset_type")
        if not menu:
            return

        menu.clear()
        self._load_asset_types(menu)
        self._refresh_chart()

    def refresh_years_menu(self):
        menu = self.menus.get("year")
        if not menu:
            return

        menu.clear()
        self._load_years(menu)
        self._refresh_chart()

    def _init_state(self):
        self.menus: dict[str, QMenuBar] = {}
        self.actions: dict[str, object] = {}
        self.state = ChartState()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self._setup_menu(layout)
        self._setup_pie_chart(layout)

    def _setup_menu(self, layout):
        menu_bar = QMenuBar(self)

        menu_loaders = {
            "charts": self._load_charts,
            "asset_type": self._load_asset_types,
            "year": self._load_years,
        }

        for key in MENU_KEYS:
            menu = menu_bar.addMenu("")
            self.menus[key] = menu
            menu_loaders[key](menu)

        layout.addWidget(menu_bar, stretch=0)

    def _setup_pie_chart(self, layout):
        self.pie_chart = PieChartWidget()
        layout.addWidget(self.pie_chart, stretch=1)

    def _load_charts(self, menu):
        self.by_assets_action = self._add_action(
            menu, t("by_assets"), "asset",
            self._on_chart_dimension_selected,
            key="by_assets"
        )

        self.by_sectors_action = self._add_action(
            menu, t("by_sectors"), "sector",
            self._on_chart_dimension_selected,
            key="by_sectors"
        )

    def _on_chart_dimension_selected(self, dimension: str):
        self.state.dimension = dimension
        self._refresh_chart()

    def _load_asset_types(self, menu):
        self.all_asset_types_action = self._add_action(
            menu, t("all"), 0, 
            self._on_asset_type_selected,
            key="all"
        )

        with get_db() as db:
            service = AssetTypeService(db)
            for asset_type in service.list_all_models():
                self._add_action(
                    menu, asset_type.name, asset_type.id,
                    self._on_asset_type_selected,
                )

    def _on_asset_type_selected(self, asset_type_id: int):
        self.state.asset_type_id = None if asset_type_id == 0 else asset_type_id
        self._refresh_chart()

    def _load_years(self, menu):
        with get_db() as db:
            service = PositionSnapshotService(db)
            min_date = service.get_earliest_snapshot_date()

        current_year = Date.today().year
        start_year = min_date.year if min_date else current_year

        earliest_allowed_year = max(start_year, current_year - 19)

        for year in range(current_year, earliest_allowed_year - 1, -1):
            self._add_action(
                menu, str(year), year,
                self._on_year_selected,
            )

    def _on_year_selected(self, year: int):
        self.state.year = year
        self._refresh_chart()

    def _add_action(self, menu, text, data, handler, *, key=None):
        action = menu.addAction(text)
        action.setData(data)
        action.triggered.connect(lambda _, v=data: handler(v))

        if key:
            self.actions[key] = action

        return action

    def _refresh_chart(self):
        if not self.state.year:
            return

        title = self._build_chart_title()
        data = self._load_chart_data()

        self.pie_chart.render_chart(
            data,
            title=title,
            no_data_text=t("no_data_available")
        )

    def _build_chart_title(self) -> str:
        asset_type_label = self._get_asset_type_label()
        key = f"allocation_by_{self.state.dimension}"

        return t(key).format(
            asset_type=asset_type_label,
            year=self.state.year,
        )

    def _get_asset_type_label(self) -> str:
        if self.state.asset_type_id is None:
            return t("all")

        return self._get_asset_type_name(self.state.asset_type_id)

    def _get_asset_type_name(self, asset_type_id: int) -> str:
        with get_db() as db:
            service = AssetTypeService(db)
            asset_type = service.get(asset_type_id)
            return asset_type.name

    def _load_chart_data(self):
        loader = self.CHART_LOADERS.get(self.state.dimension)
        if not loader:
            return []

        with get_db() as db:
            service = PositionSnapshotService(db)
            return loader(
                service,
                year=self.state.year,
                asset_type_id=self.state.asset_type_id,
            )
