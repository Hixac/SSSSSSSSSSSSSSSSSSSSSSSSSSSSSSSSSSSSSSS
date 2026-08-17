from uuid import UUID

from sqlalchemy import select

from src.core.repository import RepositoryBase
from src.models.postponed import Postponed


class PostponedRepository(RepositoryBase[Postponed]):
    async def get_by_domain(self, group_domain: str) -> list[Postponed]:
        statement = select(Postponed).where(
            Postponed.group_domain == group_domain
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, id: UUID) -> Postponed | None:
        statement = select(Postponed).where(Postponed.id == id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
