from typing import Any

import jwt
from bcrypt import (
    gensalt,
    hashpw,
    checkpw
)
from src.core.config import settings


def hash_password(password: str) -> str:
    bytes = password.encode("utf-8")
    hashed = hashpw(bytes, gensalt()).decode()

    return hashed


def verify_password(password: str, hashed_password: str) -> bool:
    return checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def jwt_encode(payload: dict[str, Any]) -> str:
    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        payload=payload, 
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def jwt_decode(encoded_jwt: str | bytes) -> dict[str, Any]:
    return jwt.decode(  # pyright: ignore[reportUnknownMemberType]
        jwt=encoded_jwt,
        key=settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()

    encoded_jwt = jwt_encode(to_encode)
    return encoded_jwt
