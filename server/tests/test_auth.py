import pytest
from uuid import UUID
from httpx import AsyncClient
from sqlalchemy.exc import NoResultFound

from src.core.database import AsyncSession
from src.core.security import jwt_decode
from src.api.v1.auth.repository import AuthSessionRepository


@pytest.mark.asyncio
class TestAuth:
    async def test_auth(
        self,
        session: AsyncSession,
        client: AsyncClient,
        sample_auth_data: dict[str, str]
    ) -> None:
        response = await client.post(
            "/api/v1/auth/register",
            json=sample_auth_data
        )
        assert response.status_code == 200

        token = response.cookies["accessToken"]
        data = jwt_decode(token)
        assert "expire_at" in data

        response = await client.get("/api/v1/auth/cookies")
        data = jwt_decode(response.json()["accessToken"])

        repo = AuthSessionRepository.from_session(session)
        _ = await repo.get_or_raise(UUID(data["id"]))

        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == 200

        with pytest.raises(NoResultFound):
            _ = await repo.get_or_raise(UUID(data["id"]))

    async def test_logout(
        self,
        client: AsyncClient
    ) -> None:
        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == 401
