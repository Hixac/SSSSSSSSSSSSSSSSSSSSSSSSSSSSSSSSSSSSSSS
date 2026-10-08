from typing import Annotated

from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from src.api.v1.auth.dependencies import verify_user
from src.models.auth_session import AuthSession
from src.redis import get_redis
from .schemas import TGChannel, TGPost
from .service import tg_service


router = APIRouter(prefix="/tg", tags=["tg"])


@router.get(
    "/channel/{domain}",
    response_model=TGChannel
)
async def channel_info(
    domain: str,
    redis: Annotated[Redis, Depends(get_redis)],
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> TGChannel:
    return await tg_service.get_channel_info(redis, domain)


@router.get(
    "/wall",
    response_model=list[TGPost]
)
async def wall(
    domain: str,
    count: int,
    offset: int,
    redis: Annotated[Redis, Depends(get_redis)],
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> list[TGPost]:
    posts = await tg_service.get_posts(redis, domain, count=count, offset=offset)
    return posts
