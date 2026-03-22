import pytest
from httpx import AsyncClient

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_running_session(session: AsyncSession):
    _ = await session.execute(text("SELECT 1"))
