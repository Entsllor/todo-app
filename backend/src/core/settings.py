from pydantic import BaseSettings
from pathlib import Path

BASE_PATH = Path(__file__)


class AppSettings(BaseSettings):
    DB_URI: str = "postgresql://user:pass@db:5432/postgres"
    SECRET_KEY: str = "YOUR SECRET KEY"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 20
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30

    class Config:
        env_file = BASE_PATH.joinpath(".env")
        env_prefix = "APP_"


settings = AppSettings()
