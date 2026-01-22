from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

class TitleWidget(QFrame):
    def __init__(self, text: str = "", parent=None):
        super().__init__(parent)

        self.setObjectName("TitleFrame")

        layout = QHBoxLayout(self)

        self.label = QLabel(text)
        self.label.setObjectName("TitleLabel")
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)

    def setText(self, text: str):
        self.label.setText(text)
