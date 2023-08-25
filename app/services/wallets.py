import json
from typing import List

from app.db.repositories.currency import CurrencyRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.wallet import WalletRepository
from app.models.wallets import Wallet
from app.utils.ExchangeRate import ExchangeRate
from app.utils.exceptions import UserNotFound, WalletNotFound, NotEnoughMoney


class Wallets:

    def __init__(self, repo, user_repo, currency_repo):
        self.repo: WalletRepository = repo
        self.user_repo: UserRepository = user_repo
        self.currency_repo: CurrencyRepository = currency_repo

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

    async def change_money(self, sender_wallet_id: int, accept_wallet_id: int, money_sum: int) -> List[Wallet]:
        wallet1 = await self.repo.get_wallet_by_id(sender_wallet_id)
        wallet2 = await self.repo.get_wallet_by_id(accept_wallet_id)

        if not any((wallet1, wallet2)):
            raise WalletNotFound
        elif wallet1.score < money_sum:
            raise NotEnoughMoney
        else:
            currency_list = await ExchangeRate.fetch_exchange_rate()
            accept_currency = await self.currency_repo.get_currency_by_id(wallet2.currency)

            currency_info = json.loads(currency_list).get("Valute").get(accept_currency.short_name)
            currency_course = round(currency_info.get("Nominal") / currency_info.get("Value"), 6)

            wallet1 = await self.repo.change_wallet_score(wallet1.id, money_sum * -1)
            wallet2 = await self.repo.change_wallet_score(wallet2.id, money_sum * currency_course)
        return [wallet1, wallet2]