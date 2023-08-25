from typing import List

from app.db import BaseRepository
from app.models.banks import Currency


class CurrencyRepository(BaseRepository):

    async def get_currencies(self) -> List[Currency]:
        result = await self.fetch_rows("SELECT * FROM currencies", serializer=Currency)
        return result
