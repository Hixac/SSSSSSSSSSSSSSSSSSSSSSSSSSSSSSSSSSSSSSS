import uuid
from datetime import datetime, UTC, timedelta


def utc_now() -> datetime:
    return datetime.now(UTC)


def utc_now_plus_hour() -> datetime:
    return datetime.now(UTC) + timedelta(hours=1)


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()
