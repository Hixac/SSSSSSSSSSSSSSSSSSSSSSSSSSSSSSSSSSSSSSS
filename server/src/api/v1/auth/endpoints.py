from typing import Annotated, Any

import structlog
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, Request, Response

from src.core.database import AsyncSession, get_db_session
from src.models.auth_session import AuthSession

from .service import auth_service
from .schemas import AuthCookie, AuthLoginSchema, AuthRegisterSchema
from .dependencies import validate_cookies, verify_user


LOGGER = structlog.get_logger()


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    status_code=200,
    responses={
        200: {"description": "Passed"},
        401: {"description": "Wrong email or password"}
    }
)
async def login(
    auth: AuthLoginSchema,
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> JSONResponse:
    return await auth_service.login(session, auth)


@router.post(
    "/register",
    responses={
        201: {"description": "Registered"},
        400: {"description": "Missing required fields or bad syntax"},
    }
)
async def register(
    auth: AuthRegisterSchema,
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> JSONResponse:  # TODO: do redirect for the fuck's sake
    return await auth_service.register(session, auth)


@router.post(
    "/logout",
    responses={
        200: {"description": "Successfully logged out"},
        401: {"description": ""}
    }
)
async def logout(
    response: Response,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    auth_session: Annotated[AuthSession, Depends(verify_user)]
) -> JSONResponse:
    response.delete_cookie(key="accessToken")
    return await auth_service.logout(session, auth_session)


@router.get("/cookies")
async def cookies(
    request: Request,
    _: Annotated[AuthSession, Depends(verify_user)]
) -> dict[str, Any]:
    return request.cookies
