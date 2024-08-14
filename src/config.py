import os
from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.docker", env_file_encoding="utf-8")

    ollama_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="phi3:mini")

    ai_strategy: str = Field(default="OLLAMA")
    anthropic_api_key: Optional[str] = Field(default=None)
    openai_api_key: Optional[str] = Field(default=None)

    postgres_server: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="app")
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    queue_processing_limit: int = Field(default=-1)
    redis_endpoint: str = Field(default="redis://localhost:6379/0")
    environment: str = Field(default="development")
    db_debug: bool = Field(default=False)

    @field_validator("ai_strategy")
    def check_ai_strategy(cls, ai_strategy: str) -> str:
        logger.debug(f"Validating ai_strategy: {ai_strategy}")
        if ai_strategy not in ["OLLAMA", "ANTHROPIC", "OPENAI"]:
            raise ValueError(
                'ai_strategy must be one of "OLLAMA", "ANTHROPIC", "OPENAI"'
            )
        return ai_strategy

    @field_validator("openai_api_key")
    def check_api_key(cls, api_key: Optional[str], info: ValidationInfo) -> Optional[str]:
        logger.debug(f"Validating openai_api_key: {api_key}")
        ai_strategy = info.data.get("ai_strategy")
        if ai_strategy == "OPENAI" and not api_key:
            raise ValueError("OPENAI_API_KEY is required when ai_strategy is OPENAI")
        return api_key

    @field_validator("anthropic_api_key")
    def check_api_key_anthropic(cls, api_key: Optional[str], info: ValidationInfo) -> Optional[str]:
        logger.debug(f"Validating anthropic_api_key: {api_key}")
        ai_strategy = info.data.get("ai_strategy")
        logger.debug(f"Current ai_strategy: {ai_strategy}")
        if ai_strategy == "ANTHROPIC":
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY is required when ai_strategy is ANTHROPIC")
        elif ai_strategy != "ANTHROPIC" and api_key:
            raise ValueError(f"ANTHROPIC_API_KEY should not be set when ai_strategy is {ai_strategy}")
        return api_key

    def get_db_url(self) -> str:
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"


def load_config():
    logger.debug("Loading configuration")
    env_vars = {key: value for key, value in os.environ.items()}
    logger.debug(f"Environment variables: {env_vars}")

    try:
        config = Config()
        logger.debug(f"Loaded config: {config.dict()}")
        return config
    except Exception as e:
        logger.exception(f"Error loading configuration: {str(e)}")
        raise


config = load_config()