import json
from typing import List

from app.db.repositories.user import UserRepository
from app.db.repositories.wallet import WalletRepository
from app.models.wallets import Wallet
from app.utils.ExchangeRate import ExchangeRate
from app.utils.exceptions import UserNotFound, WalletNotFound


class Wallets:

    def __init__(self, repo, user_repo):
        self.repo: WalletRepository = repo
        self.user_repo: UserRepository = user_repo

    async def get_wallets(self, email: str) -> List[Wallet]:
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFound
        wallets = await self.repo.get_wallets_by_user_id(user.id)
        return wallets or None

    async def create_wallet(self, email: str, currency: int):
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFound
        wallet = await self.repo.insert_wallet(user.id, currency, 0, 1)
        return wallet

    async def fill_up_wallet(self, wallet_id: int, money_sum: int):
        wallet = await self.repo.get_wallet_by_id(wallet_id)
        if not wallet:
            raise WalletNotFound
        else:
            await self.repo.change_wallet_score(wallet.id, money_sum)
            return True

    async def change_money(self, wallet_id_1: int, wallet_id_2: int, money_sum: int):
        wallet1 = await self.repo.get_wallet_by_id(wallet_id_1)
        wallet2 = await self.repo.get_wallet_by_id(wallet_id_2)

        if not any((wallet1, wallet2)):
            raise WalletNotFound
        else:
            result = await ExchangeRate.fetch_exchange_rate()
            result = json.loads(result)
            return result
