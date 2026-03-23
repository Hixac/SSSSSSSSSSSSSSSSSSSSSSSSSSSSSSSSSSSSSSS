from fastapi import APIRouter

from src.api.v1.vk.schemas import VKPost

from .service import vk_service


router = APIRouter(prefix="/vk", tags=["vk"])


@router.get(
    "/wall",
    response_model=list[VKPost]
)
async def wall(count: int = 0, offset: int = 0) -> list[VKPost]:
    posts = await vk_service.get_posts("fat_asslesd", count=count, offset=offset)
    return posts
