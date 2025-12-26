from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from holdings_tracker_desktop.ui.widgets.charts_widget import ChartsWidget
from holdings_tracker_desktop.ui.widgets.operations_widget import OperationsWidget
from holdings_tracker_desktop.ui import translations

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widgets_with_translation = []
        self._setup_window()
        self._setup_layout()
        self._setup_panels()
        self._apply_styles()

    def set_language(self, lang):
        """Change language globally and update UI text without rebuilding the window."""
        if translations.current_lang == lang:
            return

        translations.current_lang = lang
        self.translate_ui()

    def translate_ui(self):
        for widget in self.widgets_with_translation:
            widget.translate_ui()

    def _setup_window(self):
        self.setWindowTitle("Holdings Tracker")
        self.setGeometry(100, 100, 800, 600)

    def _setup_layout(self):
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.setCentralWidget(self.central_widget)

    def _setup_panels(self):
        self.left_panel = OperationsWidget(self)
        self.right_panel = ChartsWidget(self)

        self.left_panel.setObjectName("LeftPanel")
        self.right_panel.setObjectName("RightPanel")

        self.main_layout.addWidget(self.left_panel, stretch=1)
        self.main_layout.addWidget(self.right_panel, stretch=1)

    def _apply_styles(self):
        self.setStyleSheet("""
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

            QFrame#TitleFrame,
            QFrame#BodyFrame {
                border: 1px solid #cccccc;
                border-radius: 8px;
                background: #f8f8f8;
            }
                           
            QLabel#TitleLabel {
                font-size: 13pt;
                font-weight: bold;
            }

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
        """)
