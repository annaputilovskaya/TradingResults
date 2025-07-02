import logging
import os.path
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config

HOST = "https://spimex.com"
RESULTS_URL = HOST + "/markets/oil_products/trades/results"

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, "logs")

config = Config(os.path.join(BASE_DIR, ".env"))


class RunConfig(BaseModel):
    """
    Run settings.
    """

    host: str = "localhost"
    port: int = 8000


class DatabaseConfig(BaseModel):
    """
    Database settings.
    """

    DB_ENGINE: str = config("POSTGRES_ENGINE")
    DB_USER: str = config("POSTGRES_USER")
    DB_PASSWORD: str = config("POSTGRES_PASSWORD")
    DB_HOST: str = config("POSTGRES_HOST")
    DB_PORT: str = config("POSTGRES_PORT")
    DB_NAME: str = config("POSTGRES_DB")
    url: str = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    test_url: str = (
        f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/test_{DB_NAME}"
    )
    echo: bool = bool(int(config("POSTGRES_ECHO")))
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class LoggingConfig(BaseModel):
    """
    Logging settings.
    """

    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = (
        "[%(asctime)s.%(msecs)03d] %(levelname)-8s %(funcName)20s %(module)s:%(lineno)d - %(message)s"
    )

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class RedisConfig(BaseModel):
    """
    Redis settings.
    """

    REDIS_HOST: str = config("REDIS_HOST")
    REDIS_PORT: str = config("REDIS_PORT")
    redis_url: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"


class Settings(BaseSettings):
    """
    Application base settings.
    """

    model_config = SettingsConfigDict(extra="ignore")
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
