from typing import Literal

from fastapi import Request
from redis import ConnectionError, RedisError, TimeoutError
from redis.asyncio import from_url, Redis
from redis.asyncio.retry import Retry
from redis.backoff import default_backoff

from .core.config import settings


REDIS_RETRY_ON_ERRROR: list[type[RedisError]] = [ConnectionError, TimeoutError]
REDIS_RETRY = Retry(default_backoff(), retries=50)

type ProcessName = Literal["app", "rate-limit", "worker", "script"]


def create_redis(process_name: ProcessName) -> Redis:
    return from_url(
        settings.REDIS_URI,
        decode_responses=True,
        retry_on_error=REDIS_RETRY_ON_ERRROR,
        retry=REDIS_RETRY,
        client_name=process_name
    )


async def get_redis(request: Request) -> Redis:
    return request.state.redis


__all__ = [
    "REDIS_RETRY",
    "REDIS_RETRY_ON_ERRROR",
    "Redis",
    "create_redis",
    "get_redis",
]
