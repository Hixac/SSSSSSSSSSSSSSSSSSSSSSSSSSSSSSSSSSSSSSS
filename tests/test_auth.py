import pytest
from httpx import AsyncClient

from src.server.core.security import jwt_decode
from src.server.core.config import settings


@pytest.mark.asyncio
class TestAuth:
    async def test_register(
        self,
        client: AsyncClient,
        sample_user_data: dict[str, str]
    ) -> None:
        response = await client.post(
            "/api/v1/auth/register",
            json=sample_user_data
        )

        assert response.status_code == 200

        token = response.cookies["access_token"]
        data = jwt_decode(token)

        print(data)
        print(settings.SECRET_KEY)

        assert "exp" in data
