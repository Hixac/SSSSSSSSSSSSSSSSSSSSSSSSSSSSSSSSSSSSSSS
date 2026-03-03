from src.server.core.database import AsyncSession
from src.server.core.security import verify_password
from src.server.models.user import User
from src.server.api.v1.user.repository import UserRepository


class AuthService:

    async def authenticate(
        self,
        session: AsyncSession,
        *,
        email: str,
        password: str
    ) -> User | None:
        repository = UserRepository.from_session(session)
        user = await repository.get_by_email(email)

        if user is None:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user


auth_service = AuthService()
