from typing import Annotated

from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends

from src.server.core.database import AsyncSession, get_db_session
from src.server.core.exceptions import BadRequest, Unauthorized
from src.server.core.security import create_access_token

from .service import auth_service
from .schemas import AuthPasswordSchema, AuthRegisterSchema
from ..user.service import user_service


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
    auth: AuthPasswordSchema,
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> JSONResponse:
    user = await auth_service.authenticate(session, email=auth.email, password=auth.password)

    if user is None:
        raise Unauthorized("Wrong email or password")

    token = create_access_token({"email": user.email, "name": user.name, "is_superuser": user.is_superuser})

    response = JSONResponse({"access_token": token})
    response.set_cookie("access_token", token, httponly=True)

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
    token = create_access_token({"email": user.email, "name": user.name, "is_superuser": user.is_superuser})

    response = JSONResponse({"access_token": token})
    response.set_cookie("access_token", token, httponly=True)

    return response
