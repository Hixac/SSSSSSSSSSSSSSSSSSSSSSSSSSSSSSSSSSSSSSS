from typing import Annotated

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from src.core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class UserBase(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=20, examples=["Elise"])]
    surname: Annotated[str, Field(min_length=3, max_length=20, examples=["Smirnova"])]
    email: Annotated[EmailStr, Field(examples=["bad_boy@example.org"])]


class UserSchema(TimestampSchema, UserBase, UUIDSchema, PersistentDeletion):
    hashed_password: str
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    model_config = ConfigDict(extra='forbid')

    password: Annotated[str, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])]


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=3, max_length=20, examples=["Elise"])]
    surname: Annotated[str | None, Field(min_length=3, max_length=20, examples=["Smirnova"])]
    email: Annotated[EmailStr | None, Field(examples=["bad_boy@example.org"])]
