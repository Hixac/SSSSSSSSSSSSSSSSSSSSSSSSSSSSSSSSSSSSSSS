from typing import Any, Literal
import httpx

from src.api.v1.vk.schemas import VKPost
from src.core.config import settings


class VKService:
    def __init__(self) -> None:
        self.access_token = settings.VK_SERVICE_KEY
        self.vk_api_url = "https://api.vk.ru/method/"

    def _route(self, route: str) -> str:
        return self.vk_api_url + route

    async def vk_request(
        self,
        route: str,
        **kwargs: Any
    ) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.request(
                "post",
                self._route(route),
                params={
                    "access_token": self.access_token,
                    "v": "5.131"
                } | kwargs
            )

    async def get_posts(self, domain: str, offset: int = 0, count: int = 1) -> list[VKPost]:
        response = await self.vk_request(
            "wall.get",
            domain=domain,
            offset=offset,
            count=count
        )
        content = response.json()

        vkposts: list[VKPost] = []
        for item in content["response"]["items"]:
            photos_url: list[str] | None = []

            for attachment in item["attachments"]:
                if attachment["type"] == "photo":
                    photos_url.append(
                        attachment["photo"]["orig_photo"]["url"]
                    )

            if not photos_url:
                photos_url = None

            vkposts.append(
                VKPost(
                    likes=item["likes"]["count"],
                    reposts=item["reposts"]["count"],
                    views=item["views"]["count"],
                    timestamp=item["date"],
                    is_pinned=True if "is_pinned" in item and item["is_pinned"] else False,
                    text=item["text"],
                    photos_url=photos_url
                ))

        return vkposts


vk_service = VKService()
