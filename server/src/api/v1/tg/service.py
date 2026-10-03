from telethon import TelegramClient
from aiogram import Bot
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession

from src.core.config import settings
from src.api.v1.tg.schemas import TGChannel, TGPost
from src.core.exceptions import InternalServerError, ResourceNotFound, TGBotKeyIsNotProvided


class TGService:
    def __init__(self) -> None:
        if settings.TG_BOT_KEY is None:
            raise TGBotKeyIsNotProvided()
        if settings.TELEGRAM_BOT_API_PORT is not None:
            local_server = TelegramAPIServer.from_base(
                f"http://localhost:{settings.TELEGRAM_BOT_API_PORT}"
            )
            session = AiohttpSession(api=local_server)
            self.bot = Bot(token=settings.TG_BOT_KEY, session=session)
        else:
            self.bot = Bot(token=settings.TG_BOT_KEY)
        self.client = TelegramClient()


    async def get_channel_info(self, domain: str) -> TGChannel:
        try:
            chat = await self.bot.get_chat(domain)
        except ChatNotFound:
            raise ResourceNotFound("Channel is not found")
        except Exception as e:
            raise InternalServerError("dunno")

        if chat.type != 'channel':
            raise ResourceNotFound("Channel is not found")

        link = None
        if chat.photo is not None:
            file_id = chat.photo.small_file_id
            file = await self.bot.get_file(file_id)  # better to download file bc link expires
            link = f"https://api.telegram.org/file/bot{settings.TG_BOT_KEY}/{file.file_path}"

        title = "" if chat.title is None else chat.title

        return TGChannel(
            name=title,
            photo_url=link
        )

    def get_posts(
        self,
        domain: str,
        count: int,
        offset: int
    ) -> list[TGPost]:
        pass


tg_service = TGService()
