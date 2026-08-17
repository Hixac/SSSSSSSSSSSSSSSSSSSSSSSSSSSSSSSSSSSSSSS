from uuid import UUID

from src.core.database import AsyncSession
from src.models.postponed import Postponed

from .repository import PostponedRepository


class PostponedService:
    async def create(
        self,
        session: AsyncSession,
        *,
        text: str | None,
        media_path: str | None,
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

    async def get_by_id(
        self, session: AsyncSession, id: UUID,
    ) -> Postponed | None:
        repo = PostponedRepository.from_session(session)
        return await repo.get_by_id(id)


postponed_service = PostponedService()
