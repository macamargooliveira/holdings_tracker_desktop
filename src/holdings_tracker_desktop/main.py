import qtawesome as qta
import sys
import traceback

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMessageBox

from holdings_tracker_desktop.database.bootstrap import Bootstrap, BootstrapError
from holdings_tracker_desktop.ui.main_window import MainWindow
from holdings_tracker_desktop.ui.splash_screen import SplashScreen

def main():
    """
    Application entry point.
    Shows splash screen during Bootstrap initialization, then launches main window.
    """

    app = QApplication(sys.argv)

    # Show splash screen while Bootstrap runs
    splash = SplashScreen()
    splash.show()
    app.processEvents()  # Force immediate display

    try:
        Bootstrap().run()
    except BootstrapError:
        splash.close()
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
    splash.close()  # Hide splash screen before showing main window

    window.showMaximized()
    window.raise_()
    window.activateWindow()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
