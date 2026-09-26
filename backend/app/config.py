"""Application settings, loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # LLM provider
    llm_api_key: str = ""
    llm_base_url: str = ""
    llm_model: str = ""

    # Data providers
    sports_data_provider: str = "mock"
    news_provider: str = "mock"

    # Database
    database_url: str = "sqlite:///./bills_mafia.db"

    # Observability
    mlflow_enabled: bool = False
    mlflow_tracking_uri: str = ""

    # CORS
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
