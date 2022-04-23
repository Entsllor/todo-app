import os
from typing import Literal

from pydantic import BaseSettings
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent


class AppSettings(BaseSettings):
    DB_URI: str
    SECRET_KEY: str = "YOUR SECRET KEY"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 20
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30
    ALEMBIC_PATH: Path | str = BASE_PATH.parent.joinpath("migrations")

    class Config:
        env_file = BASE_PATH.joinpath(".env")
        env_prefix = "APP_"


class DevSettings(AppSettings):
    DB_URI = "postgresql://user:pass@localhost:5432/postgres"

    class Config:
        env_file = BASE_PATH.joinpath(".env")
        env_prefix = "APP_DEV_"


class TestSettings(AppSettings):
    DB_URI: str = "postgresql://user:pass@localhost:5432/test_db"

    class Config:
        env_file = BASE_PATH.joinpath(".env")
        env_prefix = "APP_TEST_"


def get_settings(mode: Literal['testings', 'development', 'production'] = None):
    if mode is None:
        mode = os.getenv("FLASK_ENV", "development").lower()
    match mode:
        case "testing":
            return TestSettings()
        case _:
            return DevSettings()
