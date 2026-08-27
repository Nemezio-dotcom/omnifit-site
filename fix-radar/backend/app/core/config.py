from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./fixradar.db"

    ai_provider: str = "heuristic"  # "heuristic" | "openai"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    google_pagespeed_api_key: str = ""
    google_search_console_credentials_json: str = ""

    crawler_max_pages: int = 200
    crawler_max_depth: int = 6
    crawler_concurrency: int = 4
    crawler_request_timeout_ms: int = 15000
    crawler_user_agent: str = "OmniFitFixRadar/1.0 (+internal audit tool)"

    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
