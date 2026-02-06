from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.server.core.database import get_db_session
from src.server.core.security import hash_password
from src.server.core.exceptions import ResourceAlreadyExists

from .schemas import UserCreate, UserSchema
from .service import user_service


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    status_code=201,
    responses={
        201: {"description": "User created"},
        409: {"model": ResourceAlreadyExists.schema()}
    }
)
async def create_user(
    user: UserCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)]
):
    user_model = await user_service.create(
        session,
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=hash_password(user.password)
    )

    return UserSchema.model_validate(user_model)


@router.get("/{id}", status_code=200)
async def read_user(
    id: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)]
):
    user = await user_service.get(session, id)

    return UserSchema.model_validate(user)
