from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import ( 
  QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy, QScrollArea, QGridLayout
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from holdings_tracker_desktop.ui.formatters import format_decimal
from itertools import cycle

COLOR_PALETTE = [ "#4E79A7", "#59A14F", "#F28E2B", "#B07AA1", 
    "#76B7B2", "#EDC948", "#9C755F", "#BAB0AC" ]

START_ANGLE = 90
DONUT_WIDTH = 0.6
ITEM_LEGEND_WIDTH = 140
EXPLODE_OFFSET = 0.08

class PieChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.legend_data: list[dict] | None = None
        self.legend_columns: int | None = None
        self.hover_index: int | None = None
        self._setup_ui()

    def render_chart(self, data: list[dict], title: str, no_data_text: str):
        self.legend_data = data
        self.legend_columns = None
        self.title_label.setText(title)

        if not data:
            self._render_no_data(no_data_text)
        else: 
            self._render_pie(data)
            self._render_legend()

        self.canvas.draw_idle()

    def eventFilter(self, obj, event):
        if (
            obj is self.legend_scroll.viewport()
            and event.type() == QEvent.Type.Resize
            and self.legend_data is not None
        ):
            self._render_legend()
        return super().eventFilter(obj, event)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        self._setup_title_frame(main_layout)
        self._setup_body_frame(main_layout)

    def _setup_title_frame(self, main_layout):
        title_frame = QFrame()
        title_frame.setObjectName("TitleFrame")
        title_layout = QHBoxLayout(title_frame)

        self.title_label = QLabel("")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        title_layout.addWidget(self.title_label)
        main_layout.addWidget(title_frame)

    def _setup_body_frame(self, main_layout):
        body_frame = QFrame()
        body_frame.setObjectName("BodyFrame")
        body_layout = QVBoxLayout(body_frame)

        self._setup_pie(body_layout)
        self._setup_legend(body_layout)

        main_layout.addWidget(body_frame, stretch=1)  

    def _setup_pie(self, body_layout):
        figure = Figure(dpi=100)
        self.canvas = FigureCanvas(figure)
        self.canvas.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.ax = figure.add_subplot(111)

        figure.subplots_adjust(
            left=0.05,
            right=0.95,
            top=0.95,
            bottom=0.05
        )

        body_layout.addWidget(self.canvas, stretch=3)

    def _setup_legend(self, body_layout):
        self.legend_scroll = QScrollArea()
        self.legend_scroll.setWidgetResizable(True)
        self.legend_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        legend_container = QWidget()
        self.legend_layout = QGridLayout(legend_container)
        self.legend_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.legend_scroll.setWidget(legend_container)

        body_layout.addWidget(self.legend_scroll, stretch=1)

        self.legend_scroll.viewport().installEventFilter(self)

    def _render_no_data(self, no_data_text: str):
        self._clear_pie_chart()
        self._clear_legend()

        self.ax.text(
            0.5,
            0.5,
            no_data_text,
            ha="center",
            va="center",
            fontsize=12,
            transform=self.ax.transAxes
        )

    def _clear_pie_chart(self):
        self.ax.clear()
        self.ax.set_axis_off()

    def _clear_legend(self):
        while self.legend_layout.count():
            item = self.legend_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _render_pie(self, data: list[dict]):
        self._clear_pie_chart()

        values = [item["value"] for item in data]
        colors = COLOR_PALETTE[:len(values)]

        explode = [0.0] * len(values)
        if self.hover_index is not None:
            explode[self.hover_index] = EXPLODE_OFFSET

        self.wedges, _ = self.ax.pie(
            values,
            colors=colors,
            startangle=START_ANGLE,
            counterclock=False,
            wedgeprops={"width": DONUT_WIDTH},
            explode=explode
        )

        self.ax.set_aspect("equal")

    def _render_legend(self):
        columns = self._calculate_legend_columns()

        if columns == self.legend_columns:
            return

        self.legend_columns = columns
        self._clear_legend()

        total = sum(item["value"] for item in self.legend_data)
        colors = cycle(COLOR_PALETTE)

        for index, item in enumerate(self.legend_data):
            percent = format_decimal(item["value"] / total * 100)
            text = f'{item["label"]} — {percent}%'

            widget = self._create_legend_item(next(colors), text, index)

            row = index // columns
            col = index % columns
            self.legend_layout.addWidget(widget, row, col)

    def _calculate_legend_columns(self) -> int:
        available_width = self.legend_scroll.viewport().width()
        return max(1, available_width // ITEM_LEGEND_WIDTH)

    def _create_legend_item(self, color: str, text: str, index: int) -> QWidget:
        layout = QHBoxLayout()

        color_box = QLabel()
        color_box.setFixedSize(12, 12)
        color_box.setStyleSheet(
            f"background-color: {color}; border-radius: 2px;"
        )

        label = QLabel(text)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        label.setWordWrap(False)

        layout.addWidget(color_box)
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        container.setCursor(Qt.PointingHandCursor)

        container.enterEvent = lambda _, i=index: self._set_hover_index(i)
        container.leaveEvent = lambda _: self._set_hover_index(None)

        return container

    def _set_hover_index(self, index: int | None):
        if self.hover_index == index:
            return

        self.hover_index = index
        self._render_pie(self.legend_data)
        self.canvas.draw_idle()
