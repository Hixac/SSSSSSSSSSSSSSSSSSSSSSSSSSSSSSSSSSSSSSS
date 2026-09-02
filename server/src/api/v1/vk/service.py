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

    def gather(self, response: httpx.Response) -> dict[str, Any]:
        content = response.json()

        if "error" in content:
            error = content["error"]
            raise ResourceNotFound(
                f"VK error {error.get('error_code')}: {error.get('error_msg')}"
            )

        return content

    async def vk_request(
        self,
        route: str,
        **kwargs: Any
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                "post",
                self._route(route),
                params={
                    "access_token": self.access_token,
                    "v": "5.131"
                } | kwargs
            )
            return self.gather(response)

    async def is_group_real(self, group: str) -> bool:
        try:
            content = await self.vk_request(
                "groups.getById",
                group_id=group,
            )
        except ResourceNotFound:
            return False

        return len(content["response"]) > 0

    async def get_group_info(self, domain: str) -> VKGroup:
        content = await self.vk_request(
            "groups.getById",
            group_id=domain,
            fields="photo_100,photo_200",
        )

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
        content = await self.vk_request(
            "wall.get",
            domain=domain,
            count=count,
            offset=offset
        )

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
