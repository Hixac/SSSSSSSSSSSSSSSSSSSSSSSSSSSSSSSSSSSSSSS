import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import AsyncMock

from src.api.v1.group.service import postponed_service
from src.api.v1.vk.service import vk_service
from src.core.database import AsyncSession


@pytest_asyncio.fixture
async def authenticated(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch,
    sample_auth_data: dict[str, str],
) -> None:
    monkeypatch.setattr(
        vk_service, "is_group_real", AsyncMock(return_value=True)
    )

    response = await client.post("/api/v1/auth/register", json=sample_auth_data)
    assert response.status_code == 200

    yield


@pytest.mark.asyncio
class TestPostponedUnauthenticated:
    async def test_create_postponed_no_auth_401(
        self, client: AsyncClient, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            vk_service, "is_group_real", AsyncMock(return_value=True)
        )

        response = await client.post(
            "/api/v1/group/somegroup/postponed/",
            data={"text": "hello"},
        )
        assert response.status_code == 401

    async def test_list_postponed_no_auth_401(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/api/v1/group/somegroup/postponed/")
        assert response.status_code == 401


@pytest.mark.asyncio
class TestPostponedAuthenticated:
    async def test_create_postponed_text_only_201(
        self, client: AsyncClient, authenticated: None,
    ) -> None:
        response = await client.post(
            "/api/v1/group/testdomain/postponed/",
            data={"text": "test postponed item"},
        )
        assert response.status_code == 201

    async def test_create_postponed_vk_not_found_400(
        self, client: AsyncClient, authenticated: None,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            vk_service, "is_group_real", AsyncMock(return_value=False)
        )

        response = await client.post(
            "/api/v1/group/fakegroup/postponed/",
            data={"text": "hello"},
        )
        assert response.status_code == 400
        assert "Group not found" in response.json()["detail"]

    async def test_create_postponed_empty_400(
        self, client: AsyncClient, authenticated: None,
    ) -> None:
        response = await client.post(
            "/api/v1/group/testdomain/postponed/",
        )
        assert response.status_code == 400
        assert "At least one" in response.json()["detail"]

    async def test_list_postponed_200(
        self, client: AsyncClient, authenticated: None,
    ) -> None:
        _ = await client.post(
            "/api/v1/group/testdomain/postponed/",
            data={"text": "item one"},
        )

        response = await client.get("/api/v1/group/testdomain/postponed/")
        assert response.status_code == 200
        data = response.json()
        assert data[0]["text"] == "item one"
        assert data[0]["group_domain"] == "testdomain"
        assert "id" in data[0]
        assert "created_at" in data[0]

    async def test_list_postponed_other_domain_empty_200(
        self, client: AsyncClient, authenticated: None,
    ) -> None:
        _ = await client.post(
            "/api/v1/group/testdomain/postponed/",
            data={"text": "item one"},
        )

        response = await client.get("/api/v1/group/otherdomain/postponed/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_postponed_media_wrong_domain_404(
        self, client: AsyncClient, authenticated: None,
        session: AsyncSession,
    ) -> None:
        item = await postponed_service.create(
            session,
            text="hello",
            media_path=None,
            group_domain="testdomain",
        )

        response = await client.get(
            f"/api/v1/group/otherdomain/postponed/{item.id}/media"
        )
        assert response.status_code == 404
