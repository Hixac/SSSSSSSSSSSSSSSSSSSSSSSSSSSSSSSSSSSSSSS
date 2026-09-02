from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.core.logger import get_logger
from src.core.database import AsyncSession
from src.core.exceptions import ResourceAlreadyExists
from src.core.security import hash_password
from src.models.user import User

from .repository import UserRepository


LOGGER = get_logger(__name__)


class UserService:

    async def get(self, session: AsyncSession, id: UUID) -> User | None:
        repository = UserRepository.from_session(session)

        return await repository.get_by_id(id)

    async def create(
        self,
        session: AsyncSession,
        *,
        name: str | None = None,
        surname: str | None = None,
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
            LOGGER.info("user.create.success", email=email)
            return created_user
        except IntegrityError:
            LOGGER.warning("user.create.constraint_violation", email=email)
            raise


user_service = UserService()
