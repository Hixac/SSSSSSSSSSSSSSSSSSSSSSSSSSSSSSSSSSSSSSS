from typing import Annotated

from fastapi import Depends, Request
from jwt import InvalidTokenError
from pydantic import ValidationError

from src.core.database import AsyncSession, get_db_session
from src.core.exceptions import NotPermitted, Unauthorized
from src.core.logger import get_logger
from src.core.security import jwt_decode
from src.core.utilities import utc_now
from src.models.auth_session import AuthSession

from .schemas import AuthCookie
from .service import auth_service


LOGGER = get_logger(__name__)


def validate_cookies(request: Request) -> AuthCookie:
    raw_cookies = request.cookies
    if not raw_cookies:
        raise Unauthorized("Cannot access to this path")

    try:
        data = jwt_decode(raw_cookies["accessToken"])
        return AuthCookie.model_validate(data)
    except KeyError:
        LOGGER.warning("auth.cookies.missing_access_token")
        raise Unauthorized("Missing access token")
    except InvalidTokenError:
        LOGGER.warning("auth.cookies.invalid_token")
        raise Unauthorized("Invalid access token")
    except ValidationError:
        LOGGER.warning("auth.cookies.invalid_payload")
        raise Unauthorized("Invalid token payload")


async def verify_user(
    cookies: Annotated[AuthCookie, Depends(validate_cookies)],
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> AuthSession:
    auth_session = await auth_service.get_session(session, cookies.id)

    if auth_session.expire_at <= utc_now():
        _ = await auth_service.logout(session, auth_session)
        raise Unauthorized()

    return auth_session


async def verify_superuser(
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> AuthSession:
    if not auth_session.user.is_superuser:
        raise NotPermitted("Superuser required")
    return auth_session
