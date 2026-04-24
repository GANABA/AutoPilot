from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Agency identity
    agency_name: str = "AutoPilot Immo"
    agency_greeting: str = "Bonjour, bienvenue !"
    agency_brand_voice: str = "professionnel et chaleureux"
    agency_escalation_email: str = ""
    agency_working_hours_start: str = "09:00"
    agency_working_hours_end: str = "19:00"
    widget_token: str = "tok_change_me"

    # LLM
    openai_api_key: str
    llm_complex_model: str = "gpt-4o"
    llm_simple_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    # Database
    database_url: str

    # Redis
    redis_url: str

    # Storage (Cloudflare R2)
    cloudflare_r2_endpoint: str = ""
    cloudflare_r2_access_key: str = ""
    cloudflare_r2_secret_key: str = ""
    cloudflare_r2_bucket: str = "autopilot-docs"

    # Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24h
    admin_email: str
    admin_password: str

    # App
    allowed_origins: str = "http://localhost:3000"
    debug: bool = False

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
