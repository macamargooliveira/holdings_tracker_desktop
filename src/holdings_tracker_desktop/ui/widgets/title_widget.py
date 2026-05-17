from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

class TitleWidget(QFrame):
    def __init__(self, text: str = "", parent=None):
        super().__init__(parent)

        self.setObjectName("TitleFrame")

        layout = QHBoxLayout(self)

        self.primary_label = QLabel(text)
        self.primary_label.setObjectName("TitleLabel")

        self.secondary_label = QLabel("")
        self.secondary_label.setObjectName("SecondaryTitleLabel")

        layout.addWidget(self.primary_label, 1, Qt.AlignCenter)
        layout.addWidget(self.secondary_label, 0, Qt.AlignRight)

    def set_primary_text(self, text: str):
        self.primary_label.setText(text)

    def set_secondary_text(self, text: str):
        self.secondary_label.setText(text)
