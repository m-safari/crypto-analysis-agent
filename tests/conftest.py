"""Shared fixtures for the whole test suite."""
import os
from pathlib import Path

import pytest

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return FIXTURES_DIR


def require_env(name: str) -> str:
    """Skip the test if an env var (e.g. an API key) is missing."""
    value = os.getenv(name)
    if not value:
        pytest.skip(f"{name} not set")
    return value
