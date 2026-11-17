import os
from dotenv import load_dotenv
from langchain_openai import *
import httpx
from app.clients.freecrypto_client import FreeCryptoClient
from app.tools.crypto_tools import FreeCryptoTools
from newsapi import NewsApiClient
from app.tools.news_tools import NewsTools


from app.container import AppContainer

def main():
    container = AppContainer()

    tools = container.tools
    # Find a specific tool
    search_news = next(
        t for t in tools if t.name == "search_news"
    )

    # Invoke manually
    result = search_news.invoke({"query": "bitcoin"})
    print(result)

    print(container.llm.invoke("say hi in 5 words").content)

if __name__ == "__main__":
    main()