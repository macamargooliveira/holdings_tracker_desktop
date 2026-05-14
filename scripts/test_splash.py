import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from holdings_tracker_desktop.ui.splash_screen import SplashScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    QTimer.singleShot(5000, app.quit)

    sys.exit(app.exec())
