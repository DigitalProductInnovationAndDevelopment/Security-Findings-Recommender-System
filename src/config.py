from typing import Any, Callable, Set

from pydantic import (
    AliasChoices,
    AmqpDsn,
    BaseModel,
    Field,
    ImportString,
    PostgresDsn,
    RedisDsn,
)

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, RedisDsn


class SubModel(BaseModel):
    foo: str = "bar"
    apple: int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ollama_url: str = Field(env="OLLAMA_URL", default="http://localhost:11434")
    ollama_model: str = Field(env="OLLAMA_MODEL", default="phi3:mini")

    postgres_server: str = Field(env="POSTGRES_SERVER", default="localhost")
    postgres_port: int = Field(env="POSTGRES_PORT", default=5432)
    postgres_db: str = Field(env="POSTGRES_DB", default="app")
    postgres_user: str = Field(env="POSTGRES_USER", default="postgres")
    postgres_password: str = Field(env="POSTGRES_PASSWORD", default="postgres")

    queue_processing_limit: int = Field(env="QUEUE_PROCESSING_LIMIT", default=10)

    redis_endpoint: RedisDsn = Field(
        env="REDIS_ENDPOINT", default="redis://localhost:6379/0"
    )

    db_debug: bool = Field(env="DB_DEBUG", default=False)


settings = Settings()


print(Settings().model_dump())
"""
{
    'auth_key': 'xxx',
    'api_key': 'xxx',
    'redis_dsn': Url('redis://user:pass@localhost:6379/1'),
    'pg_dsn': MultiHostUrl('postgres://user:pass@localhost:5432/foobar'),
    'amqp_dsn': Url('amqp://user:pass@localhost:5672/'),
    'special_function': math.cos,
    'domains': set(),
    'more_settings': {'foo': 'bar', 'apple': 1},
}
"""
