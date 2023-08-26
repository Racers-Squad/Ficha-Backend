from typing import List

from app.db import BaseRepository
from app.models.banks import Bank, Currency
from loguru import logger


class BankRepository(BaseRepository):

    async def get_bank_by_id(self, bank_id: int):
        logger.info(f"Arguments: bank_id - {bank_id}")
        bank = await self.fetch_one(f"SELECT * FROM banks WHERE id={bank_id}", serializer=Bank)
        logger.info(f"Response from db: {bank}")
        return bank

    async def get_banks(self) -> List[Bank]:
        result = await self.fetch_rows(f"SELECT * FROM banks", serializer=Bank)
        logger.info(f"Response from db: {result}")
        return result

    async def get_bank_currencies(self, bank_id: int) -> List[Currency]:
        logger.info(f"Arguments: bank_id - {bank_id}")
        result = await self.fetch_rows(f"SELECT * FROM currencies cur "
                                       f"JOIN bank_currency_match bc ON bc.currency_id=cur.id"
                                       f" WHERE bc.bank_id={bank_id}", serializer=Currency)
        logger.info(f"Response from db: {result}")
        return result

    async def get_banks_by_currency(self, currency_id: int) -> List[Bank]:
        logger.info(f"Arguments: currency_id - {currency_id}")
        result = await self.fetch_rows(f"SELECT * FROM banks b JOIN bank_currency_match bc ON bc.bank_id=b.id "
                                       f"WHERE bc.currency_id={currency_id}", serializer=Bank)
        logger.info(f"Response from db: {result}")
        return result
