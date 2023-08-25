from app.db.repositories.bank import BankRepository


class Banks:

    def __init__(self, repo):
        self.repo: BankRepository = repo

    async def get_bank_by_id(self, bank_id: int):
        result = await self.repo.get_bank_by_id(bank_id)
        return result

    async def get_banks(self):
        result = await self.repo.get_banks()
        return result
