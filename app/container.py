import os
from dotenv import load_dotenv
from langchain_openai import *
import httpx
from app.clients.freecrypto_client import FreeCryptoClient
from app.tools.crypto_tools import FreeCryptoTools
from newsapi import NewsApiClient
from app.tools.news_tools import NewsTools
from app.settings import Settings

class AppContainer:

    def __init__(self):
        self.settings = Settings()

        # Clients
        crypto_client = FreeCryptoClient(api_key=self.settings.crypto_api_key)
        news_client = NewsApiClient(api_key=self.settings.news_api_key)


        # Tools
        crypto_tools = FreeCryptoTools(crypto_client=crypto_client)
        news_tools = NewsTools(news_api_client=news_client)
        self.tools = crypto_tools.get_tools() + news_tools.get_tools()

        # LLM
        self.llm  = ChatOpenAI(
            model=self.settings.llm_model,
            temperature=0.5,
            api_key=self.settings.llm_api_key,
            base_url=self.settings.llm_base_url,
            http_client=httpx.Client(trust_env=False),
            http_async_client=httpx.AsyncClient(trust_env=False),
        )

        # # Agent
        # self.agent = create_agent(
        #     model=self.llm,
        #     tools=self.tools
        # )