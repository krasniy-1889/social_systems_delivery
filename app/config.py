from functools import lru_cache

from dotenv import load_dotenv
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    PG_URL_DSN: PostgresDsn
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_settings():
    return Settings()
