import random
import datetime

from app.db.repositories.bank import BankRepository
from app.db.repositories.cards import CardRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.wallet import WalletRepository
from app.utils.exceptions import UserNotFound, BankNotFound, WalletNotFound


class Cards:

    def __init__(self, repo, user_repo, bank_repo, wallet_repo):
        self.repo: CardRepository = repo
        self.user_repo: UserRepository = user_repo
        self.bank_repo: BankRepository = bank_repo
        self.wallet_repo: WalletRepository = wallet_repo

    async def insert_card(self, email: str, wallet_id: int, bank_id: int):
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFound
        bank = await self.bank_repo.get_bank_by_id(bank_id)
        if not bank:
            raise BankNotFound
        wallet = await self.wallet_repo.get_wallet_by_id(wallet_id)
        if not wallet:
            raise WalletNotFound
        card_number = str(random.randint(1, 5)) + ''.join(str(random.randint(0, 9)) for _ in range(15))
        result = await self.repo.insert_card(wallet.id, user.id, card_number,
                                             datetime.datetime.utcnow() + datetime.timedelta(weeks=52*4), 0, bank.id)
        return result

    async def get_cards_by_user(self, email: str):
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFound
        result = await self.repo.get_cards_by_user_id(user.id)
        return result