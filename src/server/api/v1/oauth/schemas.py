from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    EmailStr
)


class OAuthPasswordSchema(BaseModel):
    email: Annotated[EmailStr, Field(examples=["lolololol@example.com"])]
    password: Annotated[str, Field(examples=["DASDASddasj23"])]
