from uuid import UUID

from sqlalchemy import select

from src.server.core.repository import RepositoryBase
from src.server.models.user import User


class UserRepository(RepositoryBase[User]):

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(
            User.email == email
        )
        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_id(self, id: UUID) -> User | None:
        statement = select(User).where(
            User.id == id
        )
        result = await self.session.execute(statement)

        return result.scalar_one_or_none()
