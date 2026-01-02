import sys
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from holdings_tracker_desktop.ui.main_window import MainWindow
import qtawesome as qta

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    icon = qta.icon("fa5s.chart-bar")
    app.setWindowIcon(icon)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
