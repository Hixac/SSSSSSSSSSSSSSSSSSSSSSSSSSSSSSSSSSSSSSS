import typing
from datetime import datetime

from uuid import UUID

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column
)

from src.core.models import RecordModel


if typing.TYPE_CHECKING:
    from .user import User


class AuthSession(RecordModel):
    __tablename__ = "auth_sessions"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="auth_session")

    expire_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, index=True
    )
