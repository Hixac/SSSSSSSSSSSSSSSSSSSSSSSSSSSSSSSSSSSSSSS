from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    EmailStr
)


class AuthLoginSchema(BaseModel):
    email: Annotated[EmailStr, Field(examples=["lolololol@example.com"])]
    password: Annotated[str, Field(examples=["DASDASddasj23"])]


class AuthRegisterSchema(BaseModel):
    name: Annotated[str, Field(examples=["Grigory"])]
    surname: Annotated[str, Field(examples=["Perelman"])]
    email: Annotated[EmailStr, Field(examples=["lolololol@example.com"])]
    password: Annotated[str, Field(examples=["DASDASddasj23"])]
