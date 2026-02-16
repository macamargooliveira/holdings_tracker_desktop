import qtawesome as qta
import sys
import traceback

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMessageBox

from holdings_tracker_desktop.database.bootstrap import Bootstrap, BootstrapError
from holdings_tracker_desktop.ui.main_window import MainWindow

def main():
    """
    Application entry point.
    Initializes infrastructure (database, migrations, metadata)
    before starting the Qt UI.
    """

    app = QApplication(sys.argv)

    try:
        Bootstrap().run()
    except BootstrapError:
        detailed_error = traceback.format_exc()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Initialization Error")
        msg.setText("The application failed to initialize properly.")
        msg.setInformativeText("Click 'Show Details' to see the technical error.")
        msg.setDetailedText(detailed_error)
        msg.exec()

        sys.exit(1)

    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setWindowIcon(qta.icon("fa5s.chart-bar"))

    window = MainWindow()
    window.showMaximized()
    window.raise_()
    window.activateWindow()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
