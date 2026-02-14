from PySide6.QtCore import QSettings

class AppSettings:
    ORGANIZATION = "HoldingsTracker"
    APPLICATION = "DesktopApp"

    def __init__(self):
        self._settings = QSettings(self.ORGANIZATION, self.APPLICATION)

    def get_language(self) -> str:
        return self._settings.value("language", "pt_BR")

    def set_language(self, lang: str):
        self._settings.setValue("language", lang)
