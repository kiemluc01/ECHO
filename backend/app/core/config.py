from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ECHO API"
    environment: str = "local"
    database_url: str = "postgresql+psycopg://echo:echo@localhost:55432/echo"
    jwt_secret: str = "change-me"
    jwt_issuer: str = "echo-api"
    access_token_minutes: int = 15
    refresh_token_days: int = 30
    oauth_redirect_base_url: str = "http://localhost:8000/v1/auth"
    google_client_id: str | None = None
    google_client_secret: str | None = None
    apple_client_id: str | None = None
    apple_client_secret: str | None = None
    bootstrap_admin_email: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
