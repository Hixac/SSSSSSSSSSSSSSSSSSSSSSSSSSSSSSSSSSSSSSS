from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

import uuid as uuid_pkg
from datetime import datetime, UTC

from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)

    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    salt: Mapped[str] = mapped_column(String)

#    uuid: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), default_factory=uuid7, unique=True)
#    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
#    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
#    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
#    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
#    is_superuser: Mapped[bool] = mapped_column(default=False)
