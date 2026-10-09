from redis.asyncio import Redis
from telethon import TelegramClient, connection
from telethon.errors import UsernameInvalidError, UsernameNotOccupiedError
from telethon.hints import TotalList
from telethon.types import Message

from src.api.v1.media.service import media_service
from src.core.config import settings
from src.api.v1.tg.schemas import TGChannel, TGPost
from src.core.exceptions import InternalServerError, ResourceNotFound


class TGService:
    def __init__(self) -> None:
        # local_server = TelegramAPIServer.from_base(
        #     f"http://localhost:{settings.TG_BOT_API_PORT}"
        # )
        # session = AiohttpSession(api=local_server)
        # self.bot = Bot(token=settings.TG_BOT_KEY, session=session)

        if settings.MTPROTO_PROXY_HOST is None and \
                settings.MTPROTO_PROXY_PORT is None and \
                settings.MTPROTO_PROXY_SECRET is None:
            self.client = TelegramClient(
                session="bot",
                api_id=settings.TG_BOT_API_ID,
                api_hash=settings.TG_BOT_API_HASH,
            )
        else:
            self.client = TelegramClient(
                session="bot",
                api_id=settings.TG_BOT_API_ID,
                api_hash=settings.TG_BOT_API_HASH,
                connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
                proxy=(settings.MTPROTO_PROXY_HOST, settings.MTPROTO_PROXY_PORT, settings.MTPROTO_PROXY_SECRET)
            )

    async def start(self) -> None:
        await self.client.start()

    async def stop(self) -> None:
        await self.client.disconnect()

    async def get_channel_info(self, redis: Redis, domain: str) -> TGChannel:
        chat = await self.client.get_entity(domain)
        if isinstance(chat, list):
            raise InternalServerError()

        if chat.username is None:
            raise ResourceNotFound("Channel is not found")

        path = await self.client.download_profile_photo(chat, file=str(settings.WHERE_TO_STORE_MEDIA))
        url = None
        if path is not None:
            url = await media_service.generate_url(redis, path)

            return TGChannel(
                name=chat.title,
                photo_url=url
            )

    async def scrape_album(self, redis: Redis, message: Message) -> list[str]:
        if not message.media:
            return []

        if not message.grouped_id:
            path = await message.download_media(file=settings.WHERE_TO_STORE_MEDIA)
            return [await media_service.generate_url(redis, path)]

        search_ids = list(range(message.id - 10, message.id + 11))
        messages: TotalList = await self.client.get_messages(message.peer_id, ids=search_ids)  # pyright: ignore   gracefully that stupid shit

        album_photos: list[str] = []
        msg: Message
        for msg in messages:
            if (msg is not None and msg.grouped_id == message.grouped_id):
                path = await msg.download_media(file=settings.WHERE_TO_STORE_MEDIA)
                album_photos.append(
                    await media_service.generate_url(redis, path)
                )
        return album_photos

    async def create_post(self, redis: Redis, message: Message) -> TGPost:
        return TGPost(
            reactions=0 if (r := message.reactions) is None else len(r.results),
            reposts=0,
            views=0 if (v := message.views) is None else v,
            timestamp=0 if (d := message.date) is None else int(d.timestamp()),
            is_pinned=False if (p := message.pinned) is None else p,  # that's bullshit idk
            text=message.message,
            photos_url=await self.scrape_album(redis, message)
        )

    async def get_posts(
        self,
        redis: Redis,
        domain: str,
        count: int,
        offset: int
    ) -> list[TGPost]:
        try:
            # for some fucking reason it throws valueerror and not the rest but I leave it here
            entity = await self.client.get_entity(domain)
        except (ValueError, UsernameNotOccupiedError, UsernameInvalidError) as e:
            raise ResourceNotFound() from e

        messages: TotalList = await self.client.get_messages(
            entity,
            limit=count,
            add_offset=offset
        )  # pyright: ignore

        posts: list[TGPost] = []
        message: Message
        for message in messages:
            posts.append(await self.create_post(redis, message))

        return posts


tg_service = TGService()
