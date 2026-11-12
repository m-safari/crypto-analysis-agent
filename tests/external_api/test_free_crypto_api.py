"""Smoke tests for FreeCryptoAPI (https://freecryptoapi.com)."""
import pytest

from tests.conftest import require_env

BASE_URL = "https://api.freecryptoapi.com/v1"


@pytest.fixture(scope="module")
def auth_headers():
    key = require_env("FREECRYPTO_TOKEN")
    return {"Authorization": f"Bearer {key}"}


def test_get_crypto_list(http, timeout, auth_headers):
    r = http.get(f"{BASE_URL}/getCryptoList", headers=auth_headers, timeout=timeout)

    # 1. request worked
    assert r.status_code == 200, r.text

    # 2. valid JSON, non-empty
    data = r.json()
    assert data, "empty response"

    # 3. BTC is in there (loose check, works whether the payload is a list or a dict)
    assert "BTC" in r.text