from pathlib import Path
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QGuiApplication, QPixmap, QPainter, QPainterPath, QColor
import qtawesome as qta


def create_rounded_icon(icon_name: str, output_path: Path, size: int = 256) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    radius = size * 0.18
    background = QPainterPath()
    background.addRoundedRect(0, 0, size, size, radius, radius)
    painter.fillPath(background, QColor("#ffffff"))

    icon = qta.icon(icon_name, color="#000000")
    icon_size = int(size * 0.92)
    icon_pixmap = icon.pixmap(QSize(icon_size, icon_size))

    x = (size - icon_pixmap.width()) // 2
    y = (size - icon_pixmap.height()) // 2
    painter.drawPixmap(x, y, icon_pixmap)
    painter.end()

    success = pixmap.save(str(output_path), "ICO")
    if not success:
        raise RuntimeError(f"Failed to save icon to {output_path}")


if __name__ == "__main__":
    app = QGuiApplication([])
    project_root = Path(__file__).resolve().parent.parent
    icon_path = project_root / "src" / "holdings_tracker_desktop" / "ui" / "assets" / "HoldingsTracker.ico"
    create_rounded_icon("fa5s.chart-bar", icon_path)
    print(f"Created {icon_path}")
