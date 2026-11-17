import json
import requests
from app.clients.exceptions import ApiError, ApiHTTPError

DEFAULT_TIMEOUT = 10  # seconds


class BaseClient:
    def __init__(
        self,
        base_url: str,
        headers: dict | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        session: requests.Session | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.update({"Accept": "application/json", **(headers or {})})

    def _get(self, path: str, params: dict | None = None):
        """GET base_url/path and return parsed JSON. Raises ApiError on any failure."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
        except requests.RequestException as e:
            raise ApiError(f"Request to {url} failed: {e}") from e

        if not response.ok:
            raise ApiHTTPError(response.status_code, response.text)

        try:
            return json.dumps(response.json())
        except ValueError as e:
            raise ApiError(f"Response from {url} is not valid JSON") from e
