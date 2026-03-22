from typing import Annotated

import structlog
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, Response

from src.core.database import AsyncSession, get_db_session
from src.core.exceptions import BadRequest, Unauthorized
from src.core.security import create_access_token

from .service import auth_service
from .schemas import AuthLoginSchema, AuthRegisterSchema
from .dependencies import validate_cookies
from ..user.service import user_service
from ..user.schemas import UserBase


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
    user = await auth_service.authenticate(session, email=auth.email, password=auth.password)

    if user is None:
        raise Unauthorized("Wrong email or password")

    token, expire = create_access_token({
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "isSuperuser": user.is_superuser
    })

    response = JSONResponse({"accessToken": token})  # TODO: redirect
    response.set_cookie(
        key="accessToken",
        value=token,
        httponly=True,
        expires=expire
    )

    return response


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
) -> JSONResponse:
    user = await auth_service.authenticate(session, email=auth.email, password=auth.password)

    if user is not None:
        raise BadRequest("Account already existing")

    user = await user_service.create(session, name=auth.name, surname=auth.surname, email=auth.email, password=auth.password)
    token, expire = create_access_token({
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "isSuperuser": user.is_superuser
    })

    response = JSONResponse({"accessToken": token})  # TODO: redirect
    response.set_cookie(
        key="accessToken",
        value=token,
        httponly=True,
        expires=expire
    )

    return response


@router.post("/logout")
async def logout(
    response: Response
) -> JSONResponse:
    response.delete_cookie(key="accessToken")
    return JSONResponse({"message": "Logged out successfully"})


@router.get("/me")
async def me(
    cookies: Annotated[UserBase, Depends(validate_cookies)]
) -> JSONResponse:
    LOGGER.info("cookies info", cookies=cookies)
    return JSONResponse(cookies.model_dump(exclude={"exp"}))
