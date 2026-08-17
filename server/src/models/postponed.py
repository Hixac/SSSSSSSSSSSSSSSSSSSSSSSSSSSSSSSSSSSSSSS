from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.core.models import RecordModel


class Postponed(RecordModel):
    __tablename__ = "postponed_items"

    text: Mapped[str | None] = mapped_column(String(256), nullable=True)
    media_path: Mapped[str] = mapped_column(nullable=True)

    group_domain: Mapped[str] = mapped_column(String(255), index=True)
