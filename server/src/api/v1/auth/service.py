from datetime import timedelta
from fastapi.responses import JSONResponse

from src.api.v1.auth.schemas import AuthCookie, AuthLoginSchema, AuthRegisterSchema
from src.api.v1.user.repository import UserRepository
from src.api.v1.user.service import user_service
from src.core.security import verify_password, create_access_token
from src.core.exceptions import Unauthorized, BadRequest
from src.core.database import AsyncSession
from src.core.utilities import utc_now
from src.core.config import settings
from src.models.auth_session import AuthSession
from src.models.user import User

from .repository import AuthSessionRepository


class AuthService:
    async def _create_auth_session(
        self,
        session: AsyncSession,
        *,
        user: User
    ) -> JSONResponse:
        repo = AuthSessionRepository.from_session(session)
        auth_session = await repo.create(AuthSession(
            user_id=user.id,
            user=user,
            expire_at=utc_now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ), flush=True)

        token, expire = create_access_token({
            "id": str(auth_session.id)
        })

        response = JSONResponse({"accessToken": token})  # TODO: redirect
        response.set_cookie(
            key="accessToken",
            value=token,
            httponly=True,
            expires=expire
        )

        return response

    async def login(
        self,
        session: AsyncSession,
        auth: AuthLoginSchema
    ) -> JSONResponse:
        repo = UserRepository.from_session(session)
        user = await repo.get_by_email(auth.email)

        if user is None:
            raise Unauthorized("Wrong email or password")

        if not verify_password(auth.password.get_secret_value(), user.hashed_password):
            raise Unauthorized("Wrong email or password")

        return await self._create_auth_session(session, user=user)

    async def register(
        self,
        session: AsyncSession,
        auth: AuthRegisterSchema
    ) -> JSONResponse:
        repo = UserRepository.from_session(session)
        user = await repo.get_by_email(auth.email)

        if user is not None:
            raise BadRequest("Account already existing")

        user = await user_service.create(
            session,
            email=auth.email,
            password=auth.password.get_secret_value()
        )

        return await self._create_auth_session(session, user=user)

    async def logout(
        self,
        session: AsyncSession,
        auth_cookies: AuthCookie
    ) -> JSONResponse:
        repo = AuthSessionRepository.from_session(session)

        try:
            auth_session = await repo.get_or_raise(auth_cookies.id)
            await repo.delete(auth_session)
        except:
            raise Unauthorized("auth.logout.failed")

        return JSONResponse("Successfully logout")


auth_service = AuthService()
