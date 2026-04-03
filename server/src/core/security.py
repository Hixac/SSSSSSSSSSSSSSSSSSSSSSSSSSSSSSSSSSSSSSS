from typing import Any
from datetime import datetime, timedelta

import jwt
from bcrypt import (
    gensalt,
    hashpw,
    checkpw
)
from src.core.config import settings
from src.core.utilities import utc_now


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


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> tuple[str, datetime]:
    to_encode = data.copy()

    if expires_delta:
        expire = utc_now() + expires_delta
    else:
        expire = utc_now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"expire_at": expire.isoformat()})
    encoded_jwt = jwt_encode(to_encode)
    return encoded_jwt, expire
