from datetime import date
from decimal import Decimal

from holdings_tracker_desktop.ui.core import translations as i18n

def format_date(value: date) -> str:
    if not value:
        return ""

    fmt = i18n.get_date_format()

    return value.strftime(fmt)

def format_decimal(value: Decimal, decimals: int = 2) -> str:
    if value is None:
        value = Decimal("0")

    fmt = f"{{:,.{decimals}f}}"
    text = fmt.format(value)

    fmt_cfg = i18n.get_number_format()

    if fmt_cfg["decimal"] == ",":
        text = text.replace(",", "X").replace(".", ",").replace("X", ".")

    return text
