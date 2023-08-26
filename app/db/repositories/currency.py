from typing import List

from app.db import BaseRepository
from app.models.common import Id
from loguru import logger

from app.models.currencies import Currency


class CurrencyRepository(BaseRepository):

    async def get_currencies(self) -> List[Currency]:
        result = await self.fetch_rows("SELECT * FROM currencies", serializer=Currency)
        logger.info(f"Response from db: {result}")
        return result

    async def get_currency_by_id(self, currency_id: int):
        logger.info(f"Arguments: currency_id - {currency_id}")
        result = await self.fetch_one(f"SELECT * FROM currencies WHERE id={currency_id}", serializer=Currency)
        logger.info(f"Response from db: {result}")
        return result
