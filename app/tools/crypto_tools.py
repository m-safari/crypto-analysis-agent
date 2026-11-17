from langchain_core.tools import tool
from app.clients.freecrypto_client import FreeCryptoClient


class FreeCryptoTools:

    def __init__(self, crypto_client: FreeCryptoClient):
        self.crypto_client = crypto_client

    def get_tools(self) -> list:
        return [
            tool(self.crypto_list_tool),
            tool(self.crypto_data_tool),
        ]

    def crypto_list_tool(self) -> str:
        """Get list of supported cryptocurrencies and pairs.
            Args:
                No input args

            Returns:
                Retruns a clean json depicting list of supported cryptocurrencies and pairs along the status and resulted list size in the following format:
                {
                    "status": true,
                    "resultset_size": 12415,
                    "result": [
                        {
                            "id": "1",
                            "symbol": "BTC",
                            "name": "",
                            "source": "binance",
                            "ohlc_available_from": "2023-01-25",
                            "history_available_from": "2016-12-17"
                        },
                        {
                            "id": "2",
                            "symbol": "ETH",
                            "name": "",
                            "source": "binance",
                            "ohlc_available_from": "2023-01-25",
                            "history_available_from": "2016-12-18"
                        },
                    ]
            }
        """
        return self.crypto_client.get_crypto_list()

    def crypto_data_tool(self, crypto_symbol: str) -> str:
        """Get single or multiple cryptocurrencies data.
            Args:
                currency symbol: str - The symbol of the cryptocurrency to get data for (e.g., BTC, ETH, etc.)

            Returns:
                Retruns a clean json depicting currency data along request status in the following format:
                {
                    "status": "success",
                    "symbols": [
                        {
                            "symbol": "BTC",
                            "last": "64399.3",
                            "last_btc": "1",
                            "lowest": "64305.12",
                            "highest": "65525.3",
                            "date": "2026-11-17 09:42:06",
                            "daily_change_percentage": "-1.0311467894631",
                            "source_exchange": "binance"
                        }
                    ]
                }
        """
        
        return self.crypto_client.get_data(crypto_symbol)
