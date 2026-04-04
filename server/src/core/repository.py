from src.core.database import AsyncSession
from src.core.models import RecordModel


class RepositoryBase[T: RecordModel]:
    def __init__(self, session: AsyncSession):
        self.session = session

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
