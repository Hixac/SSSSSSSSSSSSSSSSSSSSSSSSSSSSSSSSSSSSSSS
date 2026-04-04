from typing import Annotated
from fastapi import Depends, Request
from pydantic import ValidationError

from src.core.database import AsyncSession, get_db_session
from src.core.security import jwt_decode
from src.core.exceptions import Unauthorized
from src.models.auth_session import AuthSession

from .service import auth_service
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


async def verify_user(
    cookies: Annotated[AuthCookie, Depends(validate_cookies)],
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> AuthSession:
    return await auth_service.get_session(session, cookies.id)
