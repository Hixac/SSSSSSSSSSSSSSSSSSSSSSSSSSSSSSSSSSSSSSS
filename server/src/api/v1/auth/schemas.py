from typing import Annotated

from uuid import UUID
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    EmailStr,
    SecretStr,
)


class AuthLoginSchema(BaseModel):
    email: EmailStr
    password: Annotated[SecretStr, Field(min_length=8)]


class AuthRegisterSchema(BaseModel):
    email: EmailStr
    password: Annotated[SecretStr, Field(min_length=8)]


class AuthCookie(BaseModel):
    id: UUID


class MeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    name: str | None = None
    surname: str | None = None
