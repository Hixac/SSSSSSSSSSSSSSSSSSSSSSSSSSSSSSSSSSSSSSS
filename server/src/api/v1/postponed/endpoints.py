from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.core.database import AsyncSession, get_db_session
from src.models.auth_session import AuthSession
from src.dependencies.file import FileValidator
from src.schemas.file import ReadFile

from ..auth.dependencies import verify_user


router = APIRouter(prefix="/postponed", tags=["postponed"])


@router.post(
    "/",
    responses={
        201: {},
        400: {},
        401: {},
        413: {}
    }
)
async def postponed(
    file: Annotated[ReadFile, Depends(FileValidator())],
    session: Annotated[AsyncSession, Depends(get_db_session)],
    auth_session: Annotated[AuthSession, Depends(verify_user)]
) -> JSONResponse:
    return JSONResponse(file.model_dump_json())
