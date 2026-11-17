"""Reads configuration (API keys) from environment variables / .env."""
import os

from dotenv import load_dotenv

from app.clients.exceptions import ConfigError

load_dotenv()


def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"Environment variable {name} is not set")
    return value
