BUTTONS = """
QPushButton {
    background-color: #f5f5f5;
    border: 1px solid #c6c6c6;
    padding: 4px 8px;
    border-radius: 6px;
    min-width: 64px;
    min-height: 20px;
    outline: none;
}

QPushButton:hover {
    background-color: #eaeaea;
}

QPushButton:pressed {
    background-color: #dcdcdc;
}

QPushButton:disabled {
    background-color: #eeeeee;
    color: #999999;
}
"""

COMBOBOXES = """
QComboBox#BrokerNoteYearComboBox {
    padding: 4px 8px;
}
"""

FRAMES = """
QFrame#TitleFrame,
QFrame#BodyFrame {
    border: 1px solid #cccccc;
    border-radius: 8px;
    background: #f8f8f8;
}
"""

LABELS = """
QLabel#TitleLabel {
    font-size: 13pt;
    font-weight: bold;
}
"""

TABLES = """
QTableWidget {
    background: #ffffff;
    border: 1px solid #dcdcdc;
    border-radius: 6px;
    gridline-color: #e0e0e0;
    selection-background-color: #0066cc;
    selection-color: white;
    outline: none;
}

QTableWidget::item {
    border: none;
}
"""

HEADERS = """
QHeaderView {
    background-color: #f2f2f2;
}

QHeaderView::section {
    background-color: #f2f2f2;
    color: #333;
    padding: 4px 8px;
    border: none;
    border-bottom: 1px solid #d0d0d0;
    font-weight: 600;
    font-size: 10.5pt;
}

QHeaderView::section:hover {
    background-color: #eaeaea;
}

QHeaderView::section:pressed {
    background-color: #dddddd;
}
"""

SCROLLS = """
QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: white;
    border-radius: 8px;
}
"""

def base_styles():
    return (
        BUTTONS +
        COMBOBOXES +
        FRAMES +
        LABELS +
        TABLES +
        HEADERS +
        SCROLLS
    )
