from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.v1.auth.dependencies import verify_user
from src.models.auth_session import AuthSession
from .schemas import VKGroup, VKPost
from .service import vk_service


router = APIRouter(prefix="/vk", tags=["vk"])


@router.get(
    "/group",
    response_model=VKGroup
)
async def group_info(
    domain: str,
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> VKGroup:
    return await vk_service.get_group_info(domain)


@router.get(
    "/wall",
    response_model=list[VKPost]
)
async def wall(
    domain: str,
    count: int,
    offset: int,
    auth_session: Annotated[AuthSession, Depends(verify_user)],
) -> list[VKPost]:
    posts = await vk_service.get_posts(domain, count=count, offset=offset)
    return posts
