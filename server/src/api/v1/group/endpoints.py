from datetime import UTC
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import AwareDatetime

from src.core.database import AsyncSession, get_db_session
from src.core.exceptions import BadRequest, ResourceNotFound
from src.core.utilities import utc_now
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
    text: Annotated[str, Form()] = "",
    media: Annotated[UploadFile | None, File()] = None,
    scheduled: Annotated[AwareDatetime, Form(default_factory=utc_now)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> JSONResponse:
    if text == "" and (media is None or media.filename is None):
        raise BadRequest("At least one of text or media is required")

    if scheduled.astimezone(UTC) < utc_now():
        raise BadRequest("Can't schedule in the past")

    media_path: str = ""
    if media is not None and media.filename is not None:
        read_file = await FileValidator().validate_file(media)
        media_path = str(read_file.path)

    _ = await postponed_service.create(
        session,
        text=text,
        media_path=media_path,
        scheduled=scheduled,
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
    item = await postponed_service.get_by_id_and_domain(session, id, domain)
    if item is None:
        raise ResourceNotFound("Postponed item not found")
    if item.media_path == "":
        raise ResourceNotFound("Postponed item has no media")

    return FileResponse(item.media_path)


@router.put("/{domain}/postponed/{id}")
async def update_postponed(
    *,
    domain: str,
    id: UUID,
    text: Annotated[str | None, Form()] = None,
    media: Annotated[UploadFile | None, File()] = None,
    delete_media: Annotated[bool, Form()] = False,
    scheduled: Annotated[AwareDatetime | None, Form()] = None,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> JSONResponse:
    if delete_media and media is not None:
        raise BadRequest("Do you want to delete media or add one be specific or fix it?")

    media_path: str = ""
    if media is not None and media.filename is not None:
        read_file = await FileValidator().validate_file(media)
        media_path = str(read_file.path)

    normalized_text = text.strip() if text is not None else None

    item = await postponed_service.update(
        session,
        id=id,
        group_domain=domain,
        text=normalized_text,
        media_path=media_path,
        delete_media=delete_media,
        scheduled=scheduled
    )

    if item is None:
        raise ResourceNotFound("Postponed item not found")


    return JSONResponse("Successfully updated")


@router.delete("/{domain}/postponed/{id}", status_code=204)
async def delete_postponed(
    *,
    domain: str,
    id: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> Response:
    item = await postponed_service.delete(
        session,
        id=id,
        group_domain=domain,
    )
    if item is None:
        raise ResourceNotFound("Postponed item not found")

    return Response(status_code=204)


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
