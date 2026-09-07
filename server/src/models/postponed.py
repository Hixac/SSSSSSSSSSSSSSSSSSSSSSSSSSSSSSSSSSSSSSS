from datetime import datetime

from sqlalchemy import TIMESTAMP, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.core.models import RecordModel


class Postponed(RecordModel):
    __tablename__ = "postponed_items"

    text: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    media_path: Mapped[str] = mapped_column(String(512), nullable=False, default="")
    scheduled: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    group_domain: Mapped[str] = mapped_column(String(255), index=True)
