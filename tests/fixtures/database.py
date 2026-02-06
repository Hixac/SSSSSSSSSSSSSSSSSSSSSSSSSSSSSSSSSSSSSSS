from collections.abc import AsyncIterator

import pytest_asyncio
from pydantic_core import Url
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import drop_database, database_exists, create_database

from src.server.core.config import settings
from src.server.core.models import Model
from src.server.core.kit.db.postgres import create_async_engine


def get_database_url(worker_id: str, driver: str = "asyncpg") -> str:
    return str(
        Url.build(
            scheme=f"postgresql+{driver}",
            username=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            path=f"testing_{worker_id}",
        )
    )


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def initialize_database(worker_id: str) -> AsyncIterator[None]:
    sync_db_url = get_database_url(worker_id, "psycopg2")

    if database_exists(sync_db_url):
        drop_database(sync_db_url)

    create_database(sync_db_url)

    engine = create_async_engine(
        dsn=get_database_url(worker_id),
        application_name="test_async",
        pool_size=settings.DB_POOL_SIZE,
        pool_recycle=settings.DB_POOL_RECYCLE_SECONDS
    )

    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    await engine.dispose()

    yield

    drop_database(sync_db_url)


@pytest_asyncio.fixture
async def session(worker_id: str) -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        dsn=get_database_url(worker_id),
        application_name="test_async",
        pool_size=settings.DB_POOL_SIZE,
        pool_recycle=settings.DB_POOL_RECYCLE_SECONDS
    )

    connection = await engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(bind=connection, expire_on_commit=False)

    yield session

    await transaction.rollback()
    await connection.close()
    await engine.dispose()
