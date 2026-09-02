from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.core.models import RecordModel


class Postponed(RecordModel):
    __tablename__ = "postponed_items"

    text: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    media_path: Mapped[str] = mapped_column(String(512), nullable=False, default="")

    group_domain: Mapped[str] = mapped_column(String(255), index=True)
