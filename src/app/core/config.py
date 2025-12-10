import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str
    PROJECT_NAME: str
    DEBUG: bool

    APP_VERSION: str = "0.0.1"

    model_config = SettingsConfigDict(
            env_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "..", ".env"),
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore",
    )

settings = Settings()
