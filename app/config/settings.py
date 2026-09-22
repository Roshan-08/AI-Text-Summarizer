from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    gemini_api_key: str
    model_name: str = "gemini-3.6-flash"
    api_version: str = "v1"
    frontend_origin: str = "http://localhost:5173"
    cache_ttl: int = Field(default=300, gt=0)
    cache_max_size: int = Field(default=100, gt=0)
    max_input_length: int = Field(default=5000, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
