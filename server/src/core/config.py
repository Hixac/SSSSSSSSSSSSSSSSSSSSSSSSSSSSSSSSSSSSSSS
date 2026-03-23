import os
from pathlib import Path
from datetime import timedelta
from enum import StrEnum

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    development = "development"
    testing = "testing"  # Used for running tests
    production = "production"



env = Environment(os.getenv("MANYS_ENV", Environment.development))
if env == Environment.testing:
    env_file = ".env.testing"
else:
    env_file = ".env"


class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


class EnvironmentSettings(BaseSettings):
    ENV: Environment = env

    def is_environment(self, environments: set[Environment]) -> bool:
        return self.ENV in environments

    def is_testing(self) -> bool:
        return self.is_environment({Environment.testing})


class UserSessionSettings(BaseSettings):
    USER_SESSION_TTL: timedelta = timedelta(days=31)


class AppSettings(BaseSettings):
    APP_NAME: str = "manyS"
    APP_VERSION: str = "0.0.1"
    DEBUG: bool

    WWW_AUTHENTICATE_REALM: str = "manyS"


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @computed_field
    @property
    def REDIS_URI(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class PostgresSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    POSTGRES_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    POSTGRES_POOL_SIZE: int = 5
    POSTGRES_SYNC_POOL_SIZE: int = 1  # Specific pool size for sync connection: since we only use it in OAuth2 router, don't waste resources.
    POSTGRES_POOL_RECYCLE_SECONDS: int = 600  # 10 minutes
    POSTGRES_COMMAND_TIMEOUT_SECONDS: float = 30.0

    POSTGRES_SYNC_PREFIX: str = "postgresql://"
    POSTGRES_ASYNC_PREFIX: str = "postgresql+asyncpg://"

    @computed_field
    @property
    def sync_postgres_uri(self) -> str:
        return f"{self.POSTGRES_SYNC_PREFIX}{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"

    @computed_field
    @property
    def async_postgres_uri(self) -> str:
        return f"{self.POSTGRES_ASYNC_PREFIX}{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"


class VKSettings(BaseSettings):
    VK_SERVICE_KEY: str | None = None


class Settings(
    AppSettings,
    PostgresSettings,
    RedisSettings,
    EnvironmentSettings,
    JWTSettings,
    UserSessionSettings,
    VKSettings
):
    LOG_LEVEL: str
    CORS_ORIGINS: list[str]

    model_config = SettingsConfigDict(
            env_file=Path(__file__).parent.parent.parent.parent.joinpath(env_file),
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore",
    )


settings = Settings()
