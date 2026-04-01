import uuid
from datetime import datetime, UTC


def utc_now() -> datetime:
    return datetime.now(UTC)


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()
