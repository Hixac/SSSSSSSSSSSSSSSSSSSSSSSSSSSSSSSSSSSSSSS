from datetime import datetime
from typing import Annotated

from uuid import UUID
from pydantic import (
    BaseModel,
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
    expire_at: datetime
