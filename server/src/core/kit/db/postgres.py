import json
from decimal import Decimal
from typing import Any

from sqlalchemy import Engine
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import (
    create_async_engine as _create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import Delete, Select, Update, delete, func, select, update
from sqlalchemy.sql.base import ExecutableOption


def _json_obj_serializer(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def json_serializer(obj: Any) -> str:
    return json.dumps(obj, default=_json_obj_serializer)


def create_async_engine(
    *,
    dsn: str,
    application_name: str | None = None,
    pool_size: int | None = None,
    pool_recycle: int | None = None,
    command_timeout: float | None = None,
    debug: bool = False,
) -> AsyncEngine:
    connect_args: dict[str, Any] = {}
    if application_name is not None:
        connect_args["server_settings"] = {"application_name": application_name}
    if command_timeout is not None:
        connect_args["command_timeout"] = command_timeout

    return _create_async_engine(
        dsn,
        echo=debug,
        connect_args=connect_args,
        pool_size=pool_size,
        pool_recycle=pool_recycle,
        json_serializer=json_serializer,
    )


def create_sync_engine(
    *,
    dsn: str,
    application_name: str | None = None,
    pool_size: int | None = None,
    pool_recycle: int | None = None,
    command_timeout: float | None = None,
    debug: bool = False,
) -> Engine:
    connect_args: dict[str, Any] = {}
    if application_name is not None:
        connect_args["application_name"] = application_name
    if command_timeout is not None:
        connect_args["options"] = f"-c statement_timeout={int(command_timeout * 1000)}"
    return _create_engine(
        dsn,
        echo=debug,
        connect_args=connect_args,
        pool_size=pool_size,
        pool_recycle=pool_recycle,
    )


type AsyncSessionMaker = async_sessionmaker[AsyncSession]


def create_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore[return-value]


type SyncSessionMaker = sessionmaker[Session]


def create_sync_sessionmaker(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)


Insert = postgresql.Insert
insert = postgresql.insert


__all__ = [
    "Delete",
    "ExecutableOption",
    "Insert",
    "Select",
    "Update",
    "delete",
    "func",
    "insert",
    "select",
    "update",

    "AsyncEngine",
    "AsyncSession",
    "AsyncSessionMaker",
    "Engine",
    "Session",
    "SyncSessionMaker",
    "create_async_engine",
    "create_async_sessionmaker",
    "create_sync_engine",
    "create_sync_sessionmaker",
]
