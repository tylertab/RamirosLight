from functools import cached_property
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .singleton import ResettableSingletonMeta


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ATHLETICS_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    project_name: str = "Pan-American Athletics Hub"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    allowed_hosts: list[str] = ["*"]
    subscription_pricing: dict[str, float] = {
        "free": 0.0,
        "premium": 12.0,
        "coach": 29.0,
    }
    subscription_currency: str = "USD"

    @cached_property
    def base_path(self) -> Path:
        return Path(__file__).resolve().parents[3]


class SettingsSingleton(metaclass=ResettableSingletonMeta):
    def __init__(self) -> None:
        self._settings = Settings()

    @property
    def instance(self) -> Settings:
        return self._settings
