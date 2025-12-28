from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PieChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def render_chart(self, data: list[dict], title: str, no_data_text: str):
        self.title_label.setText(title)
        self.ax.clear()
        self.ax.set_axis_off()

        if not data:
            self._render_no_data(no_data_text)
        else: 
            self._render_pie(data)

        self.canvas.draw_idle()

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

        self.figure = Figure(dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.ax = self.figure.add_subplot(111)

        self.figure.subplots_adjust(
            left=0.05,
            right=0.95,
            top=0.95,
            bottom=0.05
        )

        body_layout.addWidget(self.canvas)
        main_layout.addWidget(body_frame, stretch=1)  

    def _render_no_data(self, no_data_text: str):
        self.ax.text(
            0.5,
            0.5,
            no_data_text,
            ha="center",
            va="center",
            fontsize=12,
            transform=self.ax.transAxes
        )

    def _render_pie(self, data: list[dict]):
        labels = [item["label"] for item in data]
        values = [item["value"] for item in data]

        self.ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(width=0.5),
            pctdistance=0.75
        )

        self.ax.set_aspect("equal", adjustable="box")
