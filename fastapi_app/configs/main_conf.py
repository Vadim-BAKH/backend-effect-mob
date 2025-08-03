"""Главный конфигуратор сервисов."""

import logging
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

CERTS_DIR = Path("/app/certs")


LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


class LoggingConfig(BaseModel):
    """Конфигуратор логирования."""

    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        """Возвращает цифровой идентификатор уровня."""
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class AuthJWT(BaseModel):
    """Модель JWT ключа."""

    private_key_path: Path = CERTS_DIR / "jwt-private.pem"
    public_key_path: Path = CERTS_DIR / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class DatabaseConfig(BaseModel):
    """Модель pydantic базы данных."""

    url: PostgresDsn
    echo: bool = False
    pool_size: int = 20
    max_overflow: int = 10


class AppConfig(BaseModel):
    """Конфигурация приложения."""

    api_prefix: str = "/api"


class Settings(BaseSettings):
    """Базовый конфигуратор приложения."""

    logging: LoggingConfig = LoggingConfig()
    app: AppConfig = AppConfig()
    origins: Annotated[list[str], Field(default_factory=list)]
    db: DatabaseConfig
    auth_jwt: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(
        env_file=("env.template", "env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )


settings = Settings()
