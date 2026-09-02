from uuid import UUID

from pydantic import ConfigDict

from src.core.schemas import PersistentDeletion, TimestampSchema


class UserSchema(TimestampSchema, PersistentDeletion):
    id: UUID
    name: str | None = None
    surname: str | None = None
    is_superuser: bool = False

    model_config = ConfigDict(from_attributes=True)
