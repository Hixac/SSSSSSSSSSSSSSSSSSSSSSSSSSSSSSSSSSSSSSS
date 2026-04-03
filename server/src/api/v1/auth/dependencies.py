from fastapi import Request
from pydantic import ValidationError

from src.core.security import jwt_decode
from src.core.exceptions import Unauthorized
from .schemas import AuthCookie


def validate_cookies(request: Request) -> AuthCookie:
    raw_cookies = request.cookies
    if not raw_cookies:
        raise Unauthorized("Cannot access to this path")
    try:
        data = jwt_decode(raw_cookies["accessToken"])
        return AuthCookie.model_validate(data)
    except ValidationError as e:
        raise e
