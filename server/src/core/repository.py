from uuid import UUID
from sqlalchemy import select

from .database import AsyncSession


class RepositoryBase[T]:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_raise(self, id: UUID) -> T:
        statement = select(T).where(T.id == id)  # pyright: ignore

        res = await self.session.execute(statement)  # pyright: ignore
        return res.scalar_one()

    async def create(self, object: T, *, flush: bool = False) -> T:
        self.session.add(object)

        if flush:
            await self.session.flush()

        return object

    async def delete(self, object: T, *, flush: bool = False) -> None:
        await self.session.delete(object)  # нужно ли вернуть соответствующую ошибку?

        if flush:
            await self.session.flush()

    @classmethod
    def from_session(cls, session: AsyncSession):
        return cls(session)
