import typing

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import RecordModel


if typing.TYPE_CHECKING:
    from .auth_session import AuthSession


class User(RecordModel):
    __tablename__ = "users"

    name: Mapped[str | None] = mapped_column(String(30))
    surname: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    auth_session: Mapped["AuthSession"] = relationship(back_populates="user")

    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
