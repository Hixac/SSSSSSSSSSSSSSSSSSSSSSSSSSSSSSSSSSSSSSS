import os
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


class DatabaseSettings(BaseSettings):
    DB_ENGINE: str

    DB_USER: str
    DB_PASSWORD: str

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    DB_POOL_SIZE: int = 5
    DB_SYNC_POOL_SIZE: int = 1  # Specific pool size for sync connection: since we only use it in OAuth2 router, don't waste resources.
    DB_POOL_RECYCLE_SECONDS: int = 600  # 10 minutes
    DB_COMMAND_TIMEOUT_SECONDS: float = 30.0

    DB_SYNC_PREFIX: str = "postgresql://"
    DB_ASYNC_PREFIX: str = "postgresql+asyncpg://"

    @computed_field
    @property
    def SYNC_DB_URI(self) -> str:
        return f"{self.DB_SYNC_PREFIX}{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @computed_field
    @property
    def ASYNC_DB_URI(self) -> str:
        return f"{self.DB_ASYNC_PREFIX}{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(
        AppSettings,
        DatabaseSettings,
        RedisSettings,
        EnvironmentSettings,
        JWTSettings
):
    LOG_LEVEL: str
    CORS_ORIGINS: list[str]

    model_config = SettingsConfigDict(
            env_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "..", 
                                  env_file),
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore",
    )


settings = Settings()
