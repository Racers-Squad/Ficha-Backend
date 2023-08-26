from typing import List

from app.db import BaseRepository
from app.models.banks import Currency
from app.models.common import Id
from loguru import logger


class CurrencyRepository(BaseRepository):

    async def get_currencies(self) -> List[Currency]:
        result = await self.fetch_rows("SELECT * FROM currencies", serializer=Currency)
        logger.info(f"Response from db: {result}")
        return result

    async def get_currency_by_id(self, currency_id: int):
        result = await self.fetch_one(f"SELECT * FROM currencies WHERE id={currency_id}", serializer=Currency)
        logger.info(f"Response from db: {result}")
        return result
