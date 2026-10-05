from types import NoneType

from telethon import TelegramClient, connection
from telethon.hints import TotalList
from telethon.types import Message
from aiogram import Bot
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNotFound

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

        self.client = TelegramClient(
            session="bot",
            api_id=settings.TG_BOT_API_ID,
            api_hash=settings.TG_BOT_API_HASH,
            connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
            proxy=(settings.MTPROTO_PROXY_HOST, settings.MTPROTO_PROXY_PORT, settings.MTPROTO_PROXY_SECRET)
        )

    async def get_channel_info(self, domain: str) -> TGChannel:
        async with self.client:
            chat = await self.client.get_entity(domain)
            if isinstance(chat, list):
                raise InternalServerError()

            if chat.username is None:
                raise ResourceNotFound("Channel is not found")

            # TODO: ADD PHOTO

            return TGChannel(
                name=chat.title,
                photo_url=None
            )

    def _message_link(self, message: Message) -> str:
        chat = message.chat
        if chat is not None and chat.username is not None:
            return f"https://t.me/{chat.username}/{message.id}"
        return ""

    async def scrape_album(self, message: Message) -> list[str]:
        if not message.grouped_id:
            return [self._message_link(message)]

        search_ids = list(range(message.id - 10, message.id + 11))
        messages: TotalList = await self.client.get_messages(message.peer_id, ids=search_ids)

        album_photos: list[str] = []
        msg: Message
        for msg in messages:
            if (msg is not None and msg.grouped_id == message.grouped_id):
                album_photos.append(self._message_link(msg))
        return album_photos

    async def create_post(self, message: Message) -> TGPost:
        return TGPost(
            reactions=0 if (r := message.reactions) is None else len(r.results),
            reposts=0,
            views=0 if (v := message.views) is None else v,
            timestamp=0 if (d := message.date) is None else int(d.timestamp()),
            is_pinned=False if (p := message.pinned) is None else p,  # that's bullshit idk
            text=message.message,
            photos_url=await self.scrape_album(message)
        )

    async def get_posts(
        self,
        domain: str,
        count: int,
        offset: int
    ) -> list[TGPost]:
        async with self.client:
            entity = await self.client.get_entity(domain)

            messages: TotalList = await self.client.get_messages(
                entity,
                limit=count,
                add_offset=offset
            )

            posts: list[TGPost] = []
            message: Message
            for message in messages:
                posts.append(await self.create_post(message))

            return posts


tg_service = TGService()
