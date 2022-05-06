import os
from pathlib import Path
from typing import Literal

from pydantic import BaseSettings

BASE_PATH = Path(__file__).parent.parent


class AppSettings(BaseSettings):
    DEBUG: bool = False
    TESTING: bool = False
    DB_URI: str
    SECRET_KEY: str = "YOUR SECRET KEY"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 20
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30
    ALEMBIC_PATH: Path | str = BASE_PATH.parent.joinpath("migrations")
    PASSWORD_HASHING_SCHEMAS: list = ['scrypt']
    ALLOWED_ORIGINS: list[str] = ['http://localhost:3000', 'https://localhost:3000']

    class Config:
        env_file = BASE_PATH.joinpath(".env")
        env_prefix = "APP_"


class DevSettings(AppSettings):
    DEBUG: bool = True
    DB_URI = "postgresql://user:pass@localhost:5432/postgres"

    class Config:
        env_file = BASE_PATH.joinpath(".env")
        env_prefix = "APP_DEV_"


class TestSettings(AppSettings):
    DEBUG: bool = True
    TESTING: bool = True
    DB_URI: str = "postgresql://user:pass@localhost:5432/test_db"
    PASSWORD_HASHING_SCHEMAS: list = ['md5_crypt']

    class Config:
        env_file = BASE_PATH.joinpath(".env")
        env_prefix = "APP_TEST_"


_test_settings = TestSettings()
_dev_settings = DevSettings()
_prod_settings = AppSettings()


def get_settings(mode: Literal['testing', 'development', 'production'] = None):
    if mode is None:
        mode = os.getenv("FLASK_ENV", "development").lower()
    match mode:
        case "testing":
            return _test_settings
        case "production":
            return _prod_settings
        case _:
            return _dev_settings
