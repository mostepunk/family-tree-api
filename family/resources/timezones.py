from datetime import datetime
from zoneinfo import ZoneInfo

MOSCOW = ZoneInfo("Europe/Moscow")


def moscow_now():
    return datetime.now(tz=MOSCOW)
