import pytest
from httpx import AsyncClient

from src.api.v1.user.repository import UserRepository
from src.api.v1.user.service import user_service
from src.core.database import AsyncSession


@pytest.mark.asyncio
class TestUserCreateRemoved:
    async def test_create_user_endpoint_is_gone_404(
        self,
        client: AsyncClient,
        sample_user_data: dict[str, str],
    ) -> None:
        response = await client.post("/api/v1/users/", json=sample_user_data)
        assert response.status_code == 404


@pytest.mark.asyncio
class TestUserRead:
    async def test_read_user_unauthenticated_401(
        self,
        client: AsyncClient,
        session: AsyncSession,
    ) -> None:
        target = await user_service.create(
            session, email="target@example.org", password="Str1ngst!",
        )

        response = await client.get(f"/api/v1/users/{target.id}")
        assert response.status_code == 401

    async def test_read_user_not_superuser_403(
        self,
        client: AsyncClient,
        session: AsyncSession,
        sample_auth_data: dict[str, str],
    ) -> None:
        target = await user_service.create(
            session, email="target@example.org", password="Str1ngst!",
        )
        register = await client.post("/api/v1/auth/register", json=sample_auth_data)
        assert register.status_code == 200

        response = await client.get(f"/api/v1/users/{target.id}")
        assert response.status_code == 403

    async def test_read_user_superuser_200_without_password_hash(
        self,
        client: AsyncClient,
        session: AsyncSession,
        sample_auth_data: dict[str, str],
    ) -> None:
        target = await user_service.create(
            session, email="target@example.org", password="Str1ngst!",
        )
        register = await client.post("/api/v1/auth/register", json=sample_auth_data)
        assert register.status_code == 200

        repo = UserRepository.from_session(session)
        me = await repo.get_by_email(sample_auth_data["email"])
        assert me is not None
        me.is_superuser = True
        await session.flush()

        response = await client.get(f"/api/v1/users/{target.id}")
        assert response.status_code == 200

        body = response.json()
        assert "hashed_password" not in body
        assert body["id"] == str(target.id)
        assert body["is_superuser"] is False
