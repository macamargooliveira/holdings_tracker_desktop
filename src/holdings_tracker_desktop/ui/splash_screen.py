"""
Splash screen widget displayed during application startup.
Shows app icon centered.
"""

from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
import qtawesome as qta


class SplashScreen(QWidget):
    """
    Minimal splash screen shown during Bootstrap.
    Features:
    - App icon centered
    - Clean, minimal design
    - Stays on top of all windows
    """

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components."""
        # Window properties
        self.setWindowFlags(
            Qt.WindowType.SplashScreen | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icon label
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_icon()
        layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Window size and position
        self.setFixedSize(300, 200)
        self._center_on_screen()

    def _center_on_screen(self):
        """Center splash screen on primary screen."""
        from PySide6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        if screen:
            geometry = screen.geometry()
            x = (geometry.width() - self.width()) // 2
            y = (geometry.height() - self.height()) // 2
            self.move(x, y)

    def _update_icon(self):
        """Load and display icon."""
        # Try to load high-res PNG first, then ICO, then fallback to qtawesome
        assets_dir = Path(__file__).parent / "assets"
        png_path = assets_dir / "HoldingsTracker_256.png"
        ico_path = assets_dir / "HoldingsTracker.ico"
        
        if png_path.exists():
            pixmap = QPixmap(str(png_path))
            if not pixmap.isNull():
                pixmap = pixmap.scaledToWidth(128, Qt.TransformationMode.SmoothTransformation)
        elif ico_path.exists():
            pixmap = QPixmap(str(ico_path))
            if not pixmap.isNull():
                pixmap = pixmap.scaledToWidth(128, Qt.TransformationMode.SmoothTransformation)
        else:
            # Fallback: create icon from qtawesome
            icon = qta.icon("fa5s.chart-bar")
            pixmap = icon.pixmap(QSize(128, 128))

        self.icon_label.setPixmap(pixmap)
