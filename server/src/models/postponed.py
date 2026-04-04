from pathlib import Path

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from src.core.models import RecordModel


class Postponed(RecordModel):
    media_path: Mapped[Path] = mapped_column()
