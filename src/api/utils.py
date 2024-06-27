import dateutil
from datetime import datetime, timezone

def add_timezone_utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt else None
