from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.v1.auth.dependencies import verify_user
from src.models.auth_session import AuthSession
from .schemas import TGChannel, TGPost
from .service import tg_service


router = APIRouter(prefix="/tg", tags=["tg"])


@router.get(
    "/channel",
    response_model=TGChannel
)
async def channel_info(
    domain: str,
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> TGChannel:
    return await tg_service.get_channel_info(domain)


@router.get(
    "/wall",
    response_model=list[TGPost]
)
async def wall(
    domain: str,
    count: int,
    offset: int,
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> list[TGPost]:
    posts = await tg_service.get_posts(domain, count=count, offset=offset)
    return posts
