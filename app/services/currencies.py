import json

from app.db.repositories.currency import CurrencyRepository
from app.models.currencies import Course
from app.utils.ExchangeRate import ExchangeRate


class Currencies:

    def __init__(self, repo):
        self.repo: CurrencyRepository = repo

    async def get_currencies(self):
        result = await self.repo.get_currencies()
        return result

    @staticmethod
    async def get_currencies_courses():
        result = []
        data_from_bank = await ExchangeRate.fetch_exchange_rate()
        currency_list = json.loads(data_from_bank).get("Valute")
        for currency in currency_list:
            currency_info = currency_list.get(currency)
            result.append(
                Course(short_name=currency, course=round(currency_info.get("Nominal") / currency_info.get("Value"), 6))
            )
        return result
