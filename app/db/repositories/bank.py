from typing import List

from app.db import BaseRepository
from app.models.banks import Bank


class BankRepository(BaseRepository):

    async def get_bank_by_id(self, bank_id: int):
        bank = await self.fetch_one(f"SELECT * FROM banks WHERE id={bank_id}", serializer=Bank)
        return bank

    async def get_banks(self) -> List[Bank]:
        result = await self.fetch_rows(f"SELECT * FROM banks", serializer=Bank)
        return result
