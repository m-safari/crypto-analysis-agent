"""Project-specific errors, so callers never have to catch `requests` exceptions."""


class ApiError(Exception):
    """Base class for everything that goes wrong when calling an external API."""


class ApiHTTPError(ApiError):
    """The API answered with a non-2xx status code."""

    def __init__(self, status_code: int, body: str):
        super().__init__(f"HTTP {status_code}: {body[:200]}")
        self.status_code = status_code
        self.body = body


class ConfigError(Exception):
    """Missing or invalid configuration (e.g. no API key in the environment)."""
