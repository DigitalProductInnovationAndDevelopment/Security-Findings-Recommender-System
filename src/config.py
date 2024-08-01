from pydantic import (
    Field,
    ValidationInfo,
)

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

from typing import Optional


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ollama_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="phi3:mini")

    ai_strategy: Optional[str] = Field(default="OLLAMA")
    anthropic_api_key: Optional[str] = Field(default=None)
    openai_api_key: Optional[str] = Field(default=None)

    postgres_server: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="app")
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    queue_processing_limit: int = Field(default=10)
    redis_endpoint: str = Field(default="redis://localhost:6379/0")
    environment: str = Field(default="development")
    db_debug: bool = Field(default=False)

    @field_validator(
        "ai_strategy",
    )
    def check_ai_strategy(cls, ai_strategy, values):
        if ai_strategy not in ["OLLAMA", "ANTHROPIC", "OPENAI"]:
            raise ValueError(
                'ai_strategy must be one of "OLLAMA", "ANTHROPIC", "OPENAI"'
            )
        return ai_strategy

    @field_validator("openai_api_key")
    def check_api_key(cls, api_key, info: ValidationInfo):
        if info.data["ai_strategy"] == "OPENAI" and not api_key:
            raise ValueError("OPENAI_API_KEY is required when ai_strategy is OPENAI")
        return api_key

    @field_validator("anthropic_api_key")
    def check_api_key_anthropic(cls, api_key, info: ValidationInfo):
        if info.data["ai_strategy"] == "ANTHROPIC" and not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is required when ai_strategy is ANTHROPIC"
            )
        return api_key

    def get_db_url(self):
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"


config = Config()
