import httpx as httpx

from app.config import Config

config = Config()


class ExchangeRate:
    @staticmethod
    async def fetch_exchange_rate():
        async with httpx.AsyncClient() as client:
            response = await client.get(config.exchange_rate_url)
            return response.text
