import pytest
from datetime import timedelta
from uuid import UUID

from httpx import AsyncClient
from sqlalchemy.exc import NoResultFound

from src.api.v1.auth.repository import AuthSessionRepository
from src.api.v1.user.service import user_service
from src.core.database import AsyncSession
from src.core.security import jwt_decode, jwt_encode
from src.core.utilities import utc_now
from src.models.auth_session import AuthSession


def get_access_token(client: AsyncClient) -> str:
    token = client.cookies.get("accessToken")
    assert token is not None
    return token


@pytest.mark.asyncio
class TestRegister:
    async def test_register_creates_session_and_cookie(
        self,
        client: AsyncClient,
        session: AsyncSession,
        sample_auth_data: dict[str, str],
    ) -> None:
        response = await client.post("/api/v1/auth/register", json=sample_auth_data)
        assert response.status_code == 200

        token = get_access_token(client)
        data = jwt_decode(token)

        repo = AuthSessionRepository.from_session(session)
        auth_session = await repo.get_or_raise(UUID(data["id"]))
        assert auth_session.expire_at > utc_now()

    async def test_register_duplicate_email_400(
        self,
        client: AsyncClient,
        sample_auth_data: dict[str, str],
    ) -> None:
        first = await client.post("/api/v1/auth/register", json=sample_auth_data)
        assert first.status_code == 200

        second = await client.post("/api/v1/auth/register", json=sample_auth_data)
        assert second.status_code == 400

    async def test_register_short_password_422(
        self,
        client: AsyncClient,
        sample_auth_data: dict[str, str],
    ) -> None:
        response = await client.post(
            "/api/v1/auth/register",
            json={**sample_auth_data, "password": "short"},
        )
        assert response.status_code == 422


@pytest.mark.asyncio
class TestLogin:
    async def test_login_success_sets_cookie(
        self,
        client: AsyncClient,
        session: AsyncSession,
        sample_auth_data: dict[str, str],
    ) -> None:
        email = sample_auth_data["email"]
        password = sample_auth_data["password"]
        _ = await user_service.create(session, email=email, password=password)

        response = await client.post(
            "/api/v1/auth/login", json={"email": email, "password": password},
        )
        assert response.status_code == 200

        data = jwt_decode(get_access_token(client))
        repo = AuthSessionRepository.from_session(session)
        _ = await repo.get_or_raise(UUID(data["id"]))

    async def test_login_wrong_password_401(
        self,
        client: AsyncClient,
        session: AsyncSession,
        sample_auth_data: dict[str, str],
    ) -> None:
        _ = await user_service.create(
            session,
            email=sample_auth_data["email"],
            password=sample_auth_data["password"],
        )

        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": sample_auth_data["email"],
                "password": "wrongpassword123",
            },
        )
        assert response.status_code == 401

    async def test_login_unknown_email_401(
        self,
        client: AsyncClient,
        sample_auth_data: dict[str, str],
    ) -> None:
        response = await client.post("/api/v1/auth/login", json=sample_auth_data)
        assert response.status_code == 401


@pytest.mark.asyncio
class TestMe:
    async def test_me_without_auth_401(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401

    async def test_me_returns_current_user(
        self,
        client: AsyncClient,
        sample_auth_data: dict[str, str],
    ) -> None:
        _ = await client.post("/api/v1/auth/register", json=sample_auth_data)

        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 200
        assert response.json()["email"] == sample_auth_data["email"]


@pytest.mark.asyncio
class TestLogout:
    async def test_logout_without_session_401(self, client: AsyncClient) -> None:
        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == 401

    async def test_logout_deletes_session_and_cookie(
        self,
        client: AsyncClient,
        session: AsyncSession,
        sample_auth_data: dict[str, str],
    ) -> None:
        _ = await client.post("/api/v1/auth/register", json=sample_auth_data)
        session_id = UUID(jwt_decode(get_access_token(client))["id"])

        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == 200
        assert client.cookies.get("accessToken") is None

        repo = AuthSessionRepository.from_session(session)
        with pytest.raises(NoResultFound):
            _ = await repo.get_or_raise(session_id)

        me = await client.get("/api/v1/auth/me")
        assert me.status_code == 401


@pytest.mark.asyncio
class TestCookieValidation:
    async def test_other_cookie_without_access_token_401(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get(
            "/api/v1/auth/me", headers={"Cookie": "locale=ru"},
        )
        assert response.status_code == 401

    async def test_garbage_token_401(self, client: AsyncClient) -> None:
        response = await client.get(
            "/api/v1/auth/me", headers={"Cookie": "accessToken=not-a-jwt"},
        )
        assert response.status_code == 401

    async def test_tampered_token_401(self, client: AsyncClient) -> None:
        token = jwt_encode({"id": "00000000-0000-0000-0000-000000000000"})
        response = await client.get(
            "/api/v1/auth/me", headers={"Cookie": f"accessToken={token}x"},
        )
        assert response.status_code == 401

    async def test_invalid_payload_401(self, client: AsyncClient) -> None:
        token = jwt_encode({"id": "not-a-uuid"})
        response = await client.get(
            "/api/v1/auth/me", headers={"Cookie": f"accessToken={token}"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
class TestExpiredSession:
    async def test_expired_session_401_and_removed(
        self,
        client: AsyncClient,
        session: AsyncSession,
        sample_auth_data: dict[str, str],
    ) -> None:
        user = await user_service.create(
            session,
            email=sample_auth_data["email"],
            password=sample_auth_data["password"],
        )
        repo = AuthSessionRepository.from_session(session)
        auth_session = await repo.create(AuthSession(
            user_id=user.id,
            user=user,
            expire_at=utc_now() - timedelta(minutes=1),
        ), flush=True)

        token = jwt_encode({"id": str(auth_session.id)})
        response = await client.get(
            "/api/v1/auth/me", headers={"Cookie": f"accessToken={token}"},
        )
        assert response.status_code == 401

        with pytest.raises(NoResultFound):
            _ = await repo.get_or_raise(auth_session.id)
