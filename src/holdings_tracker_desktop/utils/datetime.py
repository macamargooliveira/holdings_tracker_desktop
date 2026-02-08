from datetime import datetime
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")
BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")

def to_localtime(dt: datetime | None) -> datetime | None:
    """
    Convert a datetime coming from SQLite (UTC naive)
    to Brazil local time (America/Sao_Paulo).

    Assumptions:
    - All datetimes stored in SQLite are in UTC.
    - SQLite returns naive datetime objects.
    - Naive datetimes must be interpreted as UTC.
    """
    if dt is None:
        return None

    # SQLite returns naive datetime -> assume UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    return dt.astimezone(BRAZIL_TZ)
