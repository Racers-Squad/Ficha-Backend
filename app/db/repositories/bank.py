from typing import List

from app.db import BaseRepository
from app.models.banks import Bank, Currency


class BankRepository(BaseRepository):

    async def get_bank_by_id(self, bank_id: int):
        bank = await self.fetch_one(f"SELECT * FROM banks WHERE id={bank_id}", serializer=Bank)
        return bank

    async def get_banks(self) -> List[Bank]:
        result = await self.fetch_rows(f"SELECT * FROM banks", serializer=Bank)
        return result

    async def get_bank_currencies(self, bank_id: int) -> List[Currency]:
        result = await self.fetch_rows(f"SELECT * FROM currencies cur "
                                       f"JOIN bank_currency_match bc ON bc.currency_id=cur.id"
                                       f" WHERE bc.bank_id={bank_id}", serializer=Currency)
        return result

    async def get_banks_by_currency(self, currency_id: int) -> List[Bank]:
        result = await self.fetch_rows(f"SELECT * FROM banks b JOIN bank_currency_match bc ON bc.bank_id=b.id"
                                       f"WHERE bc.currency_id={currency_id}", serializer=Bank)
        return result
