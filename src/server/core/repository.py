from .database import AsyncSession


class RepositoryBase[T]:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, object: T, *, flush: bool = False) -> T:
        self.session.add(object)

        if flush:
            await self.session.flush()

        return object

    @classmethod
    def from_session(cls, session: AsyncSession):
        return cls(session)
