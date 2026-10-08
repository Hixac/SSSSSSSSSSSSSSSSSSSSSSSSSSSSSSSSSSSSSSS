from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from redis.asyncio import Redis

from src.redis import get_redis
from .service import media_service


router = APIRouter(prefix="/media", tags=["media"])


@router.get(
    "/{id}"
)
async def media(
    id: UUID,
    redis: Annotated[Redis, Depends(get_redis)]
) -> FileResponse:
    return FileResponse(await media_service.get_pic(redis, id))
