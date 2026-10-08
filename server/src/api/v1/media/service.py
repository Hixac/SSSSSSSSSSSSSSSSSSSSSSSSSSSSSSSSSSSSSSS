from pathlib import Path
from uuid import UUID, uuid4

from redis.asyncio import Redis

from src.core.config import settings
from src.core.exceptions import ResourceAlreadyExists, ResourceNotFound


class MediaService:
    def __init__(self) -> None:
        pass

    async def generate_url(
        self,
        redis: Redis,
        path: Path
    ) -> str:
        uuid = uuid4()
        result = await redis.set(str(uuid), str(path), nx=True)

        if result is None:
            raise ResourceAlreadyExists()

        return settings.BASE_URL + f"/api/v1/media/{str(uuid)}"

    async def get_pic(
        self,
        redis: Redis,
        id: UUID
    ) -> Path:
        result = await redis.get(str(id))

        if result is None:
            raise ResourceNotFound()

        # result gonna be str bc decode_responses is True at redis.py
        return Path(settings.WHERE_TO_STORE_MEDIA / result)  # pyright: ignore


media_service = MediaService()
