import json
from collections.abc import AsyncGenerator
from decimal import Decimal
from typing import Literal, Any

from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send
from sqlalchemy import Engine as SyncEngine
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import (
    create_async_engine as _create_async_engine,
)
from sqlalchemy.orm import Session as SyncSession, sessionmaker

from src.core.config import settings


type ProcessName = Literal["app", "worker", "scheduler", "script"]
type AsyncSessionMaker = async_sessionmaker[AsyncSession]
type SyncSessionMaker = sessionmaker[SyncSession]


def create_async_sessionmaker(engine: AsyncEngine) -> AsyncSessionMaker:
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore[return-value]


def create_sync_sessionmaker(engine: SyncEngine) -> SyncSessionMaker:
    return sessionmaker(engine, expire_on_commit=False)


def _json_obj_serializer(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def json_serializer(obj: Any) -> str:
    return json.dumps(obj, default=_json_obj_serializer)


def create_async_engine(process_name: ProcessName) -> AsyncEngine:
    connect_args: dict[str, Any] = {}
    connect_args["server_settings"] = {"application_name": process_name}
    connect_args["command_timeout"] = settings.POSTGRES_COMMAND_TIMEOUT_SECONDS

    return _create_async_engine(
        url=str(settings.async_postgres_uri),
        echo=False,
        connect_args=connect_args,
        pool_size=settings.POSTGRES_POOL_SIZE,
        pool_recycle=settings.POSTGRES_POOL_RECYCLE_SECONDS,
        json_serializer=json_serializer
    )


def create_sync_engine(process_name: ProcessName) -> SyncEngine:
    connect_args: dict[str, Any] = {}
    connect_args["server_settings"] = {"application_name": process_name}
    connect_args["options"] = f"-c statement_timeout={int(settings.POSTGRES_COMMAND_TIMEOUT_SECONDS * 1000)}"

    return _create_engine(
        url=str(settings.async_postgres_uri),
        echo=False,
        connect_args=connect_args,
        pool_size=settings.POSTGRES_POOL_SIZE,
        pool_recycle=settings.POSTGRES_POOL_RECYCLE_SECONDS,
    )


class AsyncSessionMiddleware:  # чтобы прикрепить сессию
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)

        sessionmaker: AsyncSessionMaker = scope["state"]["async_sessionmaker"]
        async with sessionmaker() as session:
            scope["state"]["async_session"] = session
            await self.app(scope, receive, send)


async def get_db_sessionmaker(request: Request) -> AsyncSessionMaker:
    return request.state.async_sessionmaker


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession]:
    try:
        session = request.state.async_session
    except AttributeError as e:
        raise RuntimeError(
            "Session is not present in the request state." +
            "Did you forget to add AsyncSessionMiddleware?"
        ) from e

    try:
        yield session
    except:
        await session.rollback()
        raise
    else:
        await session.commit()


__all__ = [
    "AsyncEngine",
    "SyncEngine",
    "AsyncSession",
    "SyncSession",
    "create_async_engine",
    "create_sync_engine",
    "get_db_session",
    "get_db_sessionmaker",
]
