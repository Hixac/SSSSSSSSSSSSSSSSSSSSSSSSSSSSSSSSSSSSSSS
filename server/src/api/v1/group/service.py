from pathlib import Path
from uuid import UUID

from src.core.database import AsyncSession
from src.core.exceptions import BadRequest
from src.models.postponed import Postponed

from .repository import PostponedRepository


class PostponedService:
    async def create(
        self,
        session: AsyncSession,
        *,
        text: str,
        media_path: str,
        group_domain: str,
    ) -> Postponed:
        repo = PostponedRepository.from_session(session)
        return await repo.create(Postponed(
            text=text,
            media_path=media_path,
            group_domain=group_domain,
        ), flush=True)

    async def get_by_domain(
        self, session: AsyncSession, group_domain: str,
    ) -> list[Postponed]:
        repo = PostponedRepository.from_session(session)
        return await repo.get_by_domain(group_domain)

    async def get_by_id_and_domain(
        self, session: AsyncSession, id: UUID, group_domain: str
    ) -> Postponed | None:
        repo = PostponedRepository.from_session(session)
        return await repo.get_by_id_and_domain(id, group_domain)

    async def update(
        self,
        session: AsyncSession,
        *,
        id: UUID,
        group_domain: str,
        text: str | None,
        media_path: str,
        delete_media: bool
    ) -> Postponed | None:
        item = await self.get_by_id_and_domain(session, id, group_domain)
        if item is None:
            return None

        if text is not None and text == "" and delete_media:
             raise BadRequest("Do you want to delete post instead?")
        elif text is not None and text == "" and item.media_path == "":
             raise BadRequest("Can't delete text when media is not present.\nDo you want to delete post instead?")
        elif delete_media and text is None and item.text == "":
             raise BadRequest("Can't delete media when text is empty.\nDo you want to delete post instead?")

        if text is not None:
            item.text = text
        if media_path != "":
            self._remove_file(item.media_path)
            item.media_path = media_path

        if delete_media:
            self._remove_file(item.media_path)
            item.media_path = ""

        await session.flush()
        return item

    async def delete(
        self,
        session: AsyncSession,
        *,
        id: UUID,
        group_domain: str,
    ) -> Postponed | None:
        item = await self.get_by_id_and_domain(session, id, group_domain)
        if item is None:
            return None

        self._remove_file(item.media_path)

        repo = PostponedRepository.from_session(session)
        await repo.delete(item, flush=True)
        return item

    @staticmethod
    def _remove_file(path: str | None) -> None:
        if path is None:
            return
        try:
            Path(path).unlink(missing_ok=True)
        except OSError:
            pass


postponed_service = PostponedService()
