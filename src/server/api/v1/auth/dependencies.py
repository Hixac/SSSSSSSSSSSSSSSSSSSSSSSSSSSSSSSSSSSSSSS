from fastapi import Request
from pydantic import ValidationError

from src.server.core.exceptions import Unauthorized
from ..user.schemas import UserBase


def validate_cookies(request: Request) -> UserBase:
    raw_cookies = request.cookies
    if not raw_cookies:
        raise Unauthorized("Cannot access to this path")
    try:
        return UserBase.model_validate(raw_cookies)
    except ValidationError as e:
        raise e
