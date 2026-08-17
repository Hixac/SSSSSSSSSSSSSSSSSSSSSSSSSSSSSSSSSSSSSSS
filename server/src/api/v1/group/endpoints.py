from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from src.core.database import AsyncSession, get_db_session
from src.core.exceptions import BadRequest, ResourceNotFound
from src.dependencies.file import FileValidator
from src.models.auth_session import AuthSession

from ..auth.dependencies import verify_user
from .dependencies import validate_vk_domain
from .schemas import PostponedResponse
from .service import postponed_service


router = APIRouter(prefix="/group", tags=["group"])


@router.post("/{domain}/postponed/", status_code=201)
async def create_postponed(
    *,
    domain: Annotated[str, Depends(validate_vk_domain)],
    text: Annotated[str | None, Form()] = None,
    media: Annotated[UploadFile | None, File()] = None,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> JSONResponse:
    if text is None and (media is None or media.filename is None):
        raise BadRequest("At least one of text or media is required")

    media_path: str | None = None
    if media is not None and media.filename is not None:
        read_file = await FileValidator().validate_file(media)
        media_path = str(read_file.path)

    _ = await postponed_service.create(
        session,
        text=text,
        media_path=media_path,
        group_domain=domain,
    )

    return JSONResponse("Successfully created", status_code=201)


@router.get("/{domain}/postponed/{id}/media")
async def get_postponed_media(
    domain: str,
    id: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> FileResponse:
    item = await postponed_service.get_by_id(session, id)
    if item is None or item.group_domain != domain:
        raise ResourceNotFound("Postponed item not found")
    if item.media_path is None:
        raise ResourceNotFound("No media attached")

    return FileResponse(item.media_path)


@router.get("/{domain}/postponed/", response_model=list[PostponedResponse])
async def list_postponed(
    domain: str,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> list[PostponedResponse]:
    items = await postponed_service.get_by_domain(session, domain)

    return [
        PostponedResponse(
            id=str(item.id),
            text=item.text,
            media_path=item.media_path,
            group_domain=item.group_domain,
            created_at=item.created_at.isoformat(),
        )
        for item in items
    ]
