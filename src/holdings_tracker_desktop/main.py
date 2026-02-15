import qtawesome as qta
import sys

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
    except BootstrapError as e:
        QMessageBox.critical(
            None,
            "Initialization Error",
            f"The application failed to initialize properly:\n\n{str(e)}"
        )
        sys.exit(1)

    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setWindowIcon(qta.icon("fa5s.chart-bar"))

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
