"""Fixtures for tests that hit real external APIs."""
import pytest
import requests

DEFAULT_TIMEOUT = 10


@pytest.fixture(scope="session")
def http():
    """Shared requests session with sane defaults."""
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    yield s
    s.close()


@pytest.fixture(scope="session")
def timeout() -> int:
    return DEFAULT_TIMEOUT


def pytest_collection_modifyitems(items):
    # auto-mark everything in this dir as `external`
    for item in items:
        if "external_api" in str(item.fspath):
            item.add_marker(pytest.mark.external)
