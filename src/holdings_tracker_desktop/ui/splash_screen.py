"""
Splash screen widget displayed during application startup.
Shows loading indicator while Bootstrap initializes the database.
"""

from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QFont, QPixmap, QTransform
import qtawesome as qta


class SplashScreen(QWidget):
    """
    Custom splash screen shown during Bootstrap.
    Features:
    - App icon centered
    - "Loading..." text with rotating animation
    - Clean, minimal design
    - Stays on top of all windows
    """

    def __init__(self):
        super().__init__()
        self._rotation = 0
        self._setup_ui()
        self._setup_animation()

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
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icon label
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_icon()
        layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Loading text
        text_label = QLabel("Loading HoldingsTracker...")
        font = QFont("Segoe UI", 10)
        text_label.setFont(font)
        text_label.setStyleSheet("color: #444444;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

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

    def _setup_animation(self):
        """Setup rotating animation for icon."""
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate_icon)
        self.animation_timer.start(50)  # Update every 50ms

    def _animate_icon(self):
        """Rotate icon for animation effect."""
        self._rotation = (self._rotation + 6) % 360
        self._update_icon()

    def _update_icon(self):
        """Update icon with current rotation."""
        # Try to load from assets, fallback to qtawesome if not available
        asset_path = Path(__file__).parent / "assets" / "HoldingsTracker.ico"
        
        if asset_path.exists():
            pixmap = QPixmap(str(asset_path))
            # Resize to standard splash icon size
            if not pixmap.isNull():
                pixmap = pixmap.scaledToWidth(64, Qt.TransformationMode.SmoothTransformation)
        else:
            # Fallback: create icon from qtawesome
            icon = qta.icon("fa5s.chart-bar")
            pixmap = icon.pixmap(QSize(64, 64))
        
        # Rotate pixmap if rotation is set
        if self._rotation > 0:
            transform = QTransform()
            transform.translate(32, 32)
            transform.rotate(self._rotation)
            transform.translate(-32, -32)
            pixmap = pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        
        self.icon_label.setPixmap(pixmap)

    def closeEvent(self, event):
        """Cleanup animation when closing."""
        self.animation_timer.stop()
        super().closeEvent(event)
