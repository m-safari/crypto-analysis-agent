from clients.base import BaseClient
from clients.config import get_env


class FreeCryptoClient(BaseClient):
    BASE_URL = "https://api.freecryptoapi.com/v1"

    def __init__(self, api_key: str, **kwargs):
        super().__init__(
            base_url=self.BASE_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            **kwargs,
        )

    @classmethod
    def from_env(cls, **kwargs) -> "FreeCryptoClient":
        return cls(api_key=get_env("FREECRYPTOAPI_KEY"), **kwargs)

    def get_crypto_list(self):
        return self._get("getCryptoList")

    def get_data(self, symbol: str):
        return self._get("getData", params={"symbol": symbol})  
