"""Smoke tests for NewsAPI /v2/everything via the newsapi-python client."""
import pytest
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

from tests.conftest import require_env


@pytest.fixture(scope="module")
def client():
    return NewsApiClient(api_key=require_env("NEWSAPI_KEY"))


@pytest.fixture(scope="module")
def everything_response(client):
    return client.get_everything(
        q="bitcoin",
        language="en",
        sort_by="publishedAt",
        page_size=5,
    )


def test_everything_status_ok(everything_response):
    assert everything_response["status"] == "ok"


def test_everything_has_results(everything_response):
    assert everything_response["totalResults"] > 0
    assert len(everything_response["articles"]) > 0


def test_everything_respects_page_size(everything_response):
    assert len(everything_response["articles"]) <= 5


def test_article_schema(everything_response):
    article = everything_response["articles"][0]
    for field in ("source", "title", "url", "publishedAt"):
        assert field in article, f"missing field: {field}"
    assert article["url"].startswith("http")
    assert "name" in article["source"]


def test_invalid_api_key_raises():
    bad_client = NewsApiClient(api_key="definitely-not-a-real-key")
    with pytest.raises(NewsAPIException):
        bad_client.get_everything(q="bitcoin")