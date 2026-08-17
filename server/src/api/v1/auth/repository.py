from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.core.repository import RepositoryBase
from src.models.auth_session import AuthSession


class AuthSessionRepository(RepositoryBase[AuthSession]):
    async def get_or_raise(self, id: UUID) -> AuthSession:
        statement = (
            select(AuthSession)
            .options(selectinload(AuthSession.user))
            .where(AuthSession.id == id)
        )

        res = await self.session.execute(statement)
        return res.scalar_one()
