from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.dependencies import verify_superuser
from src.core.database import get_db_session
from src.models.auth_session import AuthSession

from .schemas import UserSchema
from .service import user_service


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}", status_code=200)
async def read_user(
    id: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    auth_session: Annotated[AuthSession, Depends(verify_superuser)]
):
    user = await user_service.get(session, id)

    return UserSchema.model_validate(user)
