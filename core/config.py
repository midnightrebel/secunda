from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Organizations Directory API"
    api_v1_prefix: str = "/api/v1"
    api_key: str = Field("secret-key", description="Static API key", alias="API_KEY")
    postgres_dsn: str = Field(
        "postgresql+asyncpg://postgres:postgres@db:5432/orgs", alias="DATABASE_URL"
    )
    echo_sql: bool = False
    max_activity_levels: int = 3
    default_page_size: int = 50
    max_page_size: int = 200

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
