from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy

class LegendItemWidget(QWidget):
    hovered = Signal(object)

    def __init__(self, color: str, text: str, index: int, parent=None):
        super().__init__(parent)
        self.index = index
        self._setup_ui(color, text)
        self.setCursor(Qt.PointingHandCursor)

    def _setup_ui(self, color, text):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

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

    def enterEvent(self, event):
        self.hovered.emit(self.index)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered.emit(None)
        super().leaveEvent(event)
