from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.server.core.logger import logging
from src.server.core.database import AsyncSession
from src.server.core.exceptions import ResourceAlreadyExists
from src.server.core.security import hash_password
from src.server.models.user import User

from .repository import UserRepository


LOGGER = logging.getLogger(__file__)


class UserService:

    async def get(self, session: AsyncSession, id: UUID) -> User | None:
        repository = UserRepository.from_session(session)

        return await repository.get_by_id(id)

    async def create(
        self,
        session: AsyncSession,
        name: str,
        surname: str,
        email: str,
        password: str
    ) -> User:
        repository = UserRepository.from_session(session)

        user = await repository.get_by_email(email)
        if user is not None:
            raise ResourceAlreadyExists()

        user_model = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hash_password(password)
        )

        try:
            created_user = await repository.create(user_model, flush=True)
            LOGGER.info("user.create.success")
            return created_user
        except IntegrityError as e:
            LOGGER.warning("user.create.contsraint_violation")
            raise


user_service = UserService()
