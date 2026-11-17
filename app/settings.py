from functools import lru_cache
from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Application
    app_name: str = "Crypto Analysis Agent"
    debug: bool = False

    # Crypto API
    crypto_api_key: str = Field(validation_alias="FREECRYPTO_TOKEN")
    crypto_base_url: str = "https://api.freecryptoapi.com/v1"
    crypto_api_timeout: int = 10

    # News API
    news_api_key: str = Field(validation_alias="NEWSAPI_KEY")
    news_api_timeout: int = 10

    # LLM
    openai_api_key: SecretStr | None = Field(
        default=None,
        validation_alias="OPENAI_API_KEY",
    )
    openrouter_api_key: SecretStr | None = Field(
        default=None,
        validation_alias="OPENROUTER_API_KEY",
    )

    llm_api_key: SecretStr | None = None
    llm_base_url: str = "https://openrouter.ai/api/v1"
    llm_model: str = "openrouter/free"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @model_validator(mode="after")
    def configure_llm(self):
        openai_key = (
            self.openai_api_key.get_secret_value().strip()
            if self.openai_api_key else ""
        )
        openrouter_key = (
            self.openrouter_api_key.get_secret_value().strip()
            if self.openrouter_api_key else ""
        )

        if openai_key:
            self.llm_api_key = SecretStr(openai_key)
            self.llm_base_url = "https://api.openai.com/v1"
            self.llm_model = "gpt-4o-mini"

        elif openrouter_key:
            self.llm_api_key = SecretStr(openrouter_key)
            self.llm_base_url = "https://openrouter.ai/api/v1"
            self.llm_model = "openrouter/free"

        else:
            raise ValueError(
                "Neither OPENAI_API_KEY nor OPENROUTER_API_KEY is configured."
            )

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
