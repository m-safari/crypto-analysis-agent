from app.clients.base import BaseClient
from app.clients.config import get_env
from app.settings import Settings

class FreeCryptoClient(BaseClient):

    def __init__(self, api_key: str, **kwargs):
        super().__init__(
            base_url=Settings().crypto_base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            **kwargs,
        )

    @classmethod
    def from_env(cls, **kwargs) -> "FreeCryptoClient":
        return cls(api_key=get_env("FREECRYPTO_TOKEN"), **kwargs)


    def get_crypto_list(self):
        return self._get("getCryptoList")

    def get_data(self, symbol: str):       
        return self._get("getData", params={"symbol": symbol})  
