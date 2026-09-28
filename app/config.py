from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "epam-dial-multi-model-orchestrator"
    app_env: str = "development"
    app_port: int = 8000

    openai_base_url: str = "http://localhost:8080/v1"
    openai_api_key: str = "dial-demo-key"
    fast_model: str = "llama3"
    reasoning_model: str = "phi3"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_model_for_route(route: Literal["support", "escalate"]) -> str:
    return get_settings().fast_model if route == "support" else get_settings().reasoning_model
