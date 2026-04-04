from uuid import UUID
from sqlalchemy import select

from src.core.repository import RepositoryBase
from src.models.auth_session import AuthSession


class AuthSessionRepository(RepositoryBase[AuthSession]):
    async def get_or_raise(self, id: UUID) -> AuthSession:
        statement = select(AuthSession).where(AuthSession.id == id)

        res = await self.session.execute(statement)
        return res.scalar_one()
