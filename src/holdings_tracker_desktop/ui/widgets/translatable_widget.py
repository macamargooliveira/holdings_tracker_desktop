from PySide6.QtWidgets import QWidget

class TranslatableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_window = self.window()
        if hasattr(main_window, "register_translatable"):
            main_window.register_translatable(self)

    def translate_ui(self):
        pass
