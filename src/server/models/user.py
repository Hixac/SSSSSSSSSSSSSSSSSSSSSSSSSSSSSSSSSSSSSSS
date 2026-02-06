from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.server.core.models import RecordModel


class User(RecordModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
