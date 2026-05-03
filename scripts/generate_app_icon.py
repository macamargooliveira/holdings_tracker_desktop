from pathlib import Path
from PySide6.QtCore import Qt, QSize, QBuffer, QIODevice
from PySide6.QtGui import QGuiApplication, QPixmap, QPainter, QPainterPath, QColor
from PIL import Image
import io
import struct
import qtawesome as qta


def save_ico_with_multiple_resolutions(images: list, output_path: Path) -> None:
    """
    Manually save multiple PIL Images as a multi-resolution ICO file.
    
    Images should be in ascending size order.
    """
    if not images:
        raise ValueError("At least one image is required")
    
    # Convert all to RGBA for consistent handling
    images = [img.convert('RGBA') for img in images]
    
    # ICO header
    ico_data = struct.pack('<HHH', 0, 1, len(images))  # reserved, type=1 (ICO), count
    
    # Calculate offsets for image data
    # Each directory entry is 16 bytes, so data starts at 6 + 16*num_images
    image_data_offset = 6 + 16 * len(images)
    
    # Build directory entries and collect image data
    current_offset = image_data_offset
    image_data_list = []
    
    for img in images:
        # Save image as PNG (portable bitmap format for ICO)
        png_buffer = io.BytesIO()
        img.save(png_buffer, format='PNG')
        png_data = png_buffer.getvalue()
        image_data_list.append(png_data)
        
        # Create directory entry
        width = img.width if img.width < 256 else 0  # 0 means 256 in ICO format
        height = img.height if img.height < 256 else 0
        colors = 0  # No color palette
        reserved = 0
        planes = 1
        bits_per_pixel = 32
        
        entry = struct.pack(
            '<BBBBHHII',
            width, height, colors, reserved,
            planes, bits_per_pixel,
            len(png_data), current_offset
        )
        ico_data += entry
        current_offset += len(png_data)
    
    # Write ICO file
    with open(output_path, 'wb') as f:
        f.write(ico_data)
        for png_data in image_data_list:
            f.write(png_data)


def create_rounded_icon(icon_name: str, output_ico_path: Path, output_png_path: Path = None) -> None:
    """
    Create a multi-resolution ICO file and optionally a high-res PNG.
    
    Args:
        icon_name: qtawesome icon name (e.g., "fa5s.chart-bar")
        output_ico_path: Path to save the multi-resolution ICO file
        output_png_path: Optional path to save a 256x256 PNG for UI display
    
    Generates 6 resolutions for ICO: 16, 32, 48, 64, 128, 256 pixels.
    This ensures crisp display in the Windows taskbar and other contexts.
    """
    output_ico_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate pixmaps for each resolution
    sizes = [16, 32, 48, 64, 128, 256]
    pil_images = []
    
    for size in sizes:
        # Create transparent pixmap
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        # Draw rounded white background
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        radius = size * 0.18
        background = QPainterPath()
        background.addRoundedRect(0, 0, size, size, radius, radius)
        painter.fillPath(background, QColor("#ffffff"))
        
        # Draw icon
        icon = qta.icon(icon_name, color="#000000")
        icon_size = int(size * 0.92)
        icon_pixmap = icon.pixmap(QSize(icon_size, icon_size))
        
        x = (size - icon_pixmap.width()) // 2
        y = (size - icon_pixmap.height()) // 2
        painter.drawPixmap(x, y, icon_pixmap)
        painter.end()
        
        # Convert QPixmap to PIL Image via PNG buffer
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        buffer.close()
        
        # Load PIL Image from buffer
        png_data = buffer.data()
        pil_img = Image.open(io.BytesIO(png_data)).convert('RGBA')
        # Make a copy to avoid issues with buffer closing
        pil_img = pil_img.copy()
        pil_images.append(pil_img)
    
    # Save all sizes to a single ICO file
    print(f"Saving ICO with {len(pil_images)} resolutions: {[f'{img.width}x{img.height}' for img in pil_images]}")
    save_ico_with_multiple_resolutions(pil_images, output_ico_path)
    print(f"Successfully saved multi-resolution ICO to {output_ico_path}")
    
    # Save 256x256 PNG for UI usage (splash screen, etc.)
    if output_png_path is None:
        output_png_path = output_ico_path.parent / "HoldingsTracker_256.png"
    
    pil_images[-1].save(str(output_png_path))
    print(f"Successfully saved high-res PNG to {output_png_path}")


if __name__ == "__main__":
    app = QGuiApplication([])
    project_root = Path(__file__).resolve().parent.parent
    icon_path = project_root / "src" / "holdings_tracker_desktop" / "ui" / "assets" / "HoldingsTracker.ico"
    png_path = project_root / "src" / "holdings_tracker_desktop" / "ui" / "assets" / "HoldingsTracker_256.png"
    create_rounded_icon("fa5s.chart-bar", icon_path, png_path)
    print(f"Created {icon_path}")
