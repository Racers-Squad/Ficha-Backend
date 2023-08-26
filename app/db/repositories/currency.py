from typing import List

from app.db import BaseRepository
from app.models.currencies import Currency


class CurrencyRepository(BaseRepository):

    async def get_currencies(self) -> List[Currency]:
        result = await self.fetch_rows("SELECT * FROM currencies", serializer=Currency)
        return result

    async def get_currency_by_id(self, currency_id: int):
        result = await self.fetch_one(f"SELECT * FROM currencies WHERE id={currency_id}", serializer=Currency)
        return result
