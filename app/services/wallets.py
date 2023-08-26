import json
from typing import List

from app.db.repositories.cards import CardRepository
from app.db.repositories.currency import CurrencyRepository
from app.db.repositories.history import HistoryRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.wallet import WalletRepository
from app.models.wallets import Wallet
from app.utils.ExchangeRate import ExchangeRate
from app.utils.TypeOperation import TypeOperation
from app.utils.exceptions import UserNotFound, WalletNotFound, NotEnoughMoney
from loguru import logger


from app.utils.exceptions import UserNotFound, WalletNotFound, NotEnoughMoney, CardNotFound


class Wallets:

    def __init__(self, repo, user_repo, currency_repo, history_repo, card_repo):
        self.repo: WalletRepository = repo
        self.user_repo: UserRepository = user_repo
        self.currency_repo: CurrencyRepository = currency_repo
        self.history_repo: HistoryRepository = history_repo
        self.card_repo: CardRepository = card_repo

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
            start_meaning = await self.repo.get_wallet_score(wallet_id)
            await self.history_repo.add_operation(wallet_id, start_meaning, money_sum, TypeOperation.REPLENISHMENT,
                                                  start_meaning + money_sum)
            await self.repo.change_wallet_score(wallet.id, money_sum)
            return True

    async def change_money(self, sender_wallet_id: int, accept_wallet_id: int, money_sum: int) -> List[Wallet]:
        sender_wallet = await self.repo.get_wallet_by_id(sender_wallet_id)
        accept_wallet = await self.repo.get_wallet_by_id(accept_wallet_id)

        if not any((sender_wallet, accept_wallet)):
            raise WalletNotFound
        elif sender_wallet.score < money_sum:
            raise NotEnoughMoney
        else:
            currency_list = await ExchangeRate.fetch_exchange_rate()
            accept_currency = await self.currency_repo.get_currency_by_id(accept_wallet.currency)

            currency_info = json.loads(currency_list).get("Valute").get(accept_currency.short_name)
            currency_course = round(currency_info.get("Nominal") / currency_info.get("Value"), 6)

            await self.history_repo.add_operation(sender_wallet_id, sender_wallet.score, money_sum * -1,
                                                  TypeOperation.TRANSFER, sender_wallet.score - money_sum)
            sender_wallet = await self.repo.change_wallet_score(sender_wallet.id, money_sum * -1)

            await self.history_repo.add_operation(accept_wallet_id, accept_wallet.score, money_sum,
                                                  TypeOperation.TRANSFER,
                                                  accept_wallet.score + money_sum)
            accept_wallet = await self.repo.change_wallet_score(accept_wallet.id, money_sum * currency_course)

        return [sender_wallet, accept_wallet]

    async def withdraw_to_card(self, wallet_id: int, card_number: str, money_sum: int):
        wallet = await self.repo.get_wallet_by_id(wallet_id)
        if not wallet:
            raise WalletNotFound

        card = await self.card_repo.get_card_by_card_number(card_number)
        if not card:
            raise CardNotFound

        if wallet.score < money_sum:
            raise NotEnoughMoney

        await self.history_repo.add_operation(wallet.id, wallet.score,
                                              money_sum * -1, TypeOperation.WITHDRAWAL, wallet.score - money_sum)

        wallet = await self.repo.change_wallet_score(wallet.id, money_sum * -1)
        card = await self.card_repo.change_card_balance_by_card_number(card_number, money_sum)
        return [wallet, card]

    async def get_wallets_history(self, email: str):
        result = []
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFound

        wallets = await self.repo.get_wallets_by_user_id(user.id)
        if not wallets:
            raise WalletNotFound
        for wallet in wallets:
            history = await self.history_repo.get_history_by_wallet_id(wallet.id)
            result.append(history)
        return result
