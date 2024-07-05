from pydantic import (
    BaseModel,
    Field,
    RedisDsn,
)

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, RedisDsn

from typing import Optional


class SubModel(BaseModel):
    foo: str = "bar"
    apple: int = 1


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ollama_url: str = Field(env="OLLAMA_URL", default="http://localhost:11434")
    ollama_model: str = Field(env="OLLAMA_MODEL", default="phi3:mini")
    anthropic_api_key: Optional[str] = Field(env="ANTHROPIC_API_KEY", default=None)
    openai_api_key: Optional[str] = Field(env="OPENAI_API_KEY", default=None)

    ai_strategy: Optional[str] = Field(env="AI_STRATEGY", default="OLLAMA")

    postgres_server: str = Field(env="POSTGRES_SERVER", default="localhost")
    postgres_port: int = Field(env="POSTGRES_PORT", default=5432)
    postgres_db: str = Field(env="POSTGRES_DB", default="app")
    postgres_user: str = Field(env="POSTGRES_USER", default="postgres")
    postgres_password: str = Field(env="POSTGRES_PASSWORD", default="postgres")
    queue_processing_limit: int = Field(env="QUEUE_PROCESSING_LIMIT", default=10)
    redis_endpoint: RedisDsn = Field(
        env="REDIS_ENDPOINT", default="redis://localhost:6379/0"
    )
    environment: str = Field(env="ENVIRONMENT", default="development")
    db_debug: bool = Field(env="DB_DEBUG", default=False)

    def get_db_url(self):
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"


config = Config()
