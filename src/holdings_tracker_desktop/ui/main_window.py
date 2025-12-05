from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from holdings_tracker_desktop.ui.charts.charts_widget import ChartsWidget
from holdings_tracker_desktop.ui.operations.operations_widget import OperationsWidget
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
        self.main_layout.setContentsMargins(0, 0, 0, 0)
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
            QWidget {
                font-size: 14px;
            }

            QPushButton {
                background-color: #f5f5f5;
                border: 1px solid #c6c6c6;
                padding: 6px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #eaeaea;
            }
            QPushButton:pressed {
                background-color: #dcdcdc;
            }

            QFrame#TitleFrame {
                border: 1px solid #cccccc;
                border-radius: 6px;
                background: #f8f8f8;
            }

            QFrame#BodyFrame {
                border: 1px solid #cccccc;
                border-radius: 6px;
                background: #f8f8f8;
            }
                           
            QLabel#TitleLabel {
                font-size: 20px;
                font-weight: bold;
            }

            QTableWidget {
                background: #ffffff;
                border: 1px solid #dcdcdc;
                gridline-color: #e0e0e0;
                selection-background-color: #0066cc;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #efefef;
                padding: 5px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
            }
        """)
