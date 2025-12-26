from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QLabel, QFrame, QHeaderView, QMessageBox, QDialog
)
from holdings_tracker_desktop.ui.translations import t
from holdings_tracker_desktop.ui.confirm_dialog import ConfirmDialog
import qtawesome as qta

DEFAULT_ACTIONS = ("add", "edit", "delete")

BUTTONS_CONFIG = {
    "add": "fa5s.plus",
    "edit": "fa5s.edit",
    "delete": "fa5s.trash"
}

class EntityManagerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_state()
        self._setup_ui()

    def translate_ui(self):
        for action in self.get_enabled_actions():
            self.buttons[action].setText(t(action))

        for name, _, _ in self.get_extra_buttons():
            self.buttons[name].setText(t(name))

    def load_data(self): raise NotImplementedError
    
    def open_new_form(self): raise NotImplementedError
    
    def open_edit_form(self): raise NotImplementedError

    def delete_record(self): raise NotImplementedError

    def get_selected_id(self):
        row = self.table.currentRow()
        if row < 0: 
            return None
        return self.table.item(row, 0).data(Qt.UserRole)

    def on_add_clicked(self):
        self.open_new_form()

    def on_edit_clicked(self):
        selected_id = self.get_selected_id()
        if selected_id:
            self.open_edit_form(selected_id)

    def on_delete_clicked(self):
        selected_id = self.get_selected_id()
        if selected_id:
            self.delete_record(selected_id)

    def show_warning(self, message: str):
        QMessageBox.warning(self, "Warning", message)

    def show_error(self, message: str):
        QMessageBox.critical(self, "Error", message)

    def ask_confirmation(self, title: str, message: str) -> bool:
        dialog = ConfirmDialog(
            title=title,
            message=message,
            parent=self
        )
        return dialog.exec() == QDialog.Accepted

    def get_operations_widget(self):
        parent = self.parent()
        while parent is not None:
            if parent.__class__.__name__ == "OperationsWidget":
                return parent
            parent = parent.parent()
        return None

    def navigate_to(self, widget_cls, *args, **kwargs):
        operations = self.get_operations_widget()
        if operations:
            operations.show_widget(widget_cls, *args, **kwargs)

    def get_enabled_actions(self) -> tuple[str, ...]:
        """
        Override in subclasses to enable/disable default CRUD actions.
        """
        return DEFAULT_ACTIONS

    def get_extra_buttons(self):
        return []

    def _init_state(self):
        self.window().widgets_with_translation.append(self)
        self.buttons = {}

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 5, 0, 0)
        main_layout.setSpacing(5)

        self._setup_title_frame(main_layout)
        self._setup_body_frame(main_layout)

    def _setup_title_frame(self, main_layout):
        title_frame = QFrame()
        title_frame.setObjectName("TitleFrame")
        title_layout = QHBoxLayout(title_frame)

        self.title_label = QLabel("")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        title_layout.addWidget(self.title_label)
        main_layout.addWidget(title_frame)

    def _setup_body_frame(self, main_layout):
        body_frame = QFrame()
        body_frame.setObjectName("BodyFrame")
        body_layout = QVBoxLayout(body_frame)

        self._setup_toolbar(body_layout)
        self._setup_table(body_layout)

        main_layout.addWidget(body_frame)

    def _setup_toolbar(self, body_layout):
        toolbar = QHBoxLayout()
        toolbar.addStretch()

        for action in self.get_enabled_actions():
            icon = BUTTONS_CONFIG[action]

            button = QPushButton("")
            button.setIcon(qta.icon(icon))
            self.buttons[action] = button
            toolbar.addWidget(button)

            handler = getattr(self, f"on_{action}_clicked", None)
            if handler:
                button.clicked.connect(handler)

        for name, icon, handler in self.get_extra_buttons():
            button = QPushButton("")
            button.setIcon(qta.icon(icon))
            self.buttons[name] = button
            toolbar.addWidget(button)
            button.clicked.connect(handler)

        body_layout.addLayout(toolbar)

    def _setup_table(self, body_layout):
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        body_layout.addWidget(self.table)
