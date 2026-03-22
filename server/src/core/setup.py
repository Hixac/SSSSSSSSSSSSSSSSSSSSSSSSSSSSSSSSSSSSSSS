from typing import TypedDict
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from src.redis import Redis, create_redis
from src.core.config import settings
from src.core.database import (
    AsyncEngine,
    AsyncSessionMiddleware,
    SyncEngine,
    create_async_engine,
    create_sync_engine
)
from src.core.kit.db.postgres import (
    AsyncSessionMaker,
    SyncSessionMaker,
    create_async_sessionmaker,
    create_sync_sessionmaker,
)
from src.core.logger import structlog  # TODO: fix logger
from src.core.exception_handlers import add_exception_handlers

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware


LOGGER = structlog.getLogger(__file__)


class State(TypedDict):
    async_engine: AsyncEngine
    async_sessionmaker: AsyncSessionMaker
    sync_engine: SyncEngine
    sync_sessionmaker: SyncSessionMaker

    redis: Redis


@asynccontextmanager
async def lifespan(api: FastAPI) -> AsyncIterator[State]:  # pyright: ignore[reportUnusedParameter]
    LOGGER.info("Starting manyS API")

    async_engine = create_async_engine("app")
    async_sessionmaker = create_async_sessionmaker(async_engine)

    sync_engine = create_sync_engine("app")
    sync_sessionmaker = create_sync_sessionmaker(sync_engine)

    redis = create_redis("app")

    yield {
        "async_engine": async_engine,
        "async_sessionmaker": async_sessionmaker,
        "sync_engine": sync_engine,
        "sync_sessionmaker": sync_sessionmaker,
        "redis": redis,
    }

    await redis.aclose(True)
    await async_engine.dispose()
    sync_engine.dispose()

    LOGGER.info("manyS API stopped")


def create_application(router: APIRouter) -> FastAPI:
    application = FastAPI(lifespan=lifespan, title=settings.APP_NAME, debug=settings.DEBUG)
    application.include_router(router)

    if not settings.is_testing():
        application.add_middleware(AsyncSessionMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exception_handlers(application)

    return application
