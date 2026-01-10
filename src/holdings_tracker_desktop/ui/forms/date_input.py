from PySide6.QtWidgets import QDateEdit
from PySide6.QtCore import QDate, QLocale
import holdings_tracker_desktop.ui.translations as i18n

LOCALES = {
    "pt_BR": QLocale(QLocale.Portuguese, QLocale.Brazil),
    "en_US": QLocale(QLocale.English, QLocale.UnitedStates)
}

class DateInput(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())
        self._configure_format()

    def _configure_format(self):
        fmt = i18n.get_date_format()
        qt_format = fmt.replace("%d", "dd").replace("%m", "MM").replace("%Y", "yyyy")
        self.setDisplayFormat(qt_format)

        locale = LOCALES.get(i18n.current_lang, QLocale(QLocale.English, QLocale.UnitedStates))
        self.setLocale(locale)
