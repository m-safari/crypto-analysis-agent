from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from langchain_core.tools import tool

class NewsTools:

    def __init__(self, news_api_client: NewsApiClient):
        self.news_api_client = news_api_client


    def get_tools(self) -> list:
        return [
            tool(self.search_news),
        ]

    def search_news(self, query = '', max_items: int = 5) -> dict:
        """Get news articles based on a search query.
            Args:
                query: str - The search query for news articles.
                max_items: int - The maximum number of news articles to return (default is 5).

            Returns:
                A clean JSON depicting the news articles along with their details.
        """
        try: 
            result = self.news_api_client.get_everything(
                q = query or "bitcoin",
                language = "en",
                sort_by = "publishedAt",
                page_size = 5,
            )

            articles = [
            {
                "title": a["title"],
                "source": a["source"]["name"],
                "url": a["url"],
                "publishedAt": a["publishedAt"],
            }
            for a in result.get("articles", [])[:max_items]
            ]

            return {
                "status": result.get("status"),
                "totalResults": result.get("totalResults"),
                "returned": len(articles),
                "articles": articles,
            }

        except NewsAPIException as e:
            return {"status": "error", "message": str(e)}
