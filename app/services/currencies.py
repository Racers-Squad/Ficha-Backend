from app.db.repositories.currency import CurrencyRepository


class Currencies:

    def __init__(self, repo):
        self.repo: CurrencyRepository = repo

    async def get_currencies(self):
        result = await self.repo.get_currencies()
        return result
