from fastapi import APIRouter

from src.api.v1.vk.schemas import VKGroup, VKPost

from .service import vk_service


router = APIRouter(prefix="/vk", tags=["vk"])


@router.get(
    "/group",
    response_model=VKGroup
)
async def group_info(domain: str) -> VKGroup:
    return await vk_service.get_group_info(domain)


@router.get(
    "/wall",
    response_model=list[VKPost]
)
async def wall(domain: str, count: int, offset: int) -> list[VKPost]:
    posts = await vk_service.get_posts(domain, count=count, offset=offset)
    return posts
