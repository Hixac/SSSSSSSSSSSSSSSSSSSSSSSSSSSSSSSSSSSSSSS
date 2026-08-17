from typing import Any
import httpx

from src.api.v1.vk.schemas import VKGroup, VKPost
from src.core.config import settings
from src.core.exceptions import ResourceNotFound


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

    async def is_group_real(self, group: str) -> bool:
        response = await self.vk_request(
            "groups.getById",
            group_id=group,
        )
        content = response.json()
        if len(content["response"]) > 0:
            return True

        return False

    async def get_group_info(self, domain: str) -> VKGroup:
        response = await self.vk_request(
            "groups.getById",
            group_id=domain,
            fields="photo_100,photo_200",
        )
        content = response.json()

        response_data = content["response"]
        if isinstance(response_data, dict):
            groups = response_data.get("groups", [])
        else:
            groups = response_data

        if len(groups) == 0:
            raise ResourceNotFound("No group found")

        group = groups[0]
        return VKGroup(
            name=group["name"],
            photo_url=group.get("photo_200") or group.get("photo_100"),
        )

    async def get_posts(self, domain: str, count: int, offset: int) -> list[VKPost]:
        response = await self.vk_request(
            "wall.get",
            domain=domain,
            count=count,
            offset=offset
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
