from fastapi import Depends

from app.db.repositories.bank import BankRepository
from app.db.repositories.cards import CardsRepository
from app.db.repositories.currency import CurrencyRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.wallet import WalletRepository
from app.dependencies.db import get_repository
from app.services.banks import Banks
from app.services.cards import Cards
from app.services.currencies import Currencies
from app.services.users import Users
from app.services.wallets import Wallets


def get_user_service(repo: UserRepository = Depends(get_repository(UserRepository))):
    return Users(repo)


def get_wallet_service(repo: WalletRepository = Depends(get_repository(WalletRepository)),
                       user_repo: UserRepository = Depends(get_repository(UserRepository)),
                       currency_repo: CurrencyRepository = Depends(get_repository(CurrencyRepository))):
    return Wallets(repo, user_repo, currency_repo)


def get_bank_service(repo: BankRepository = Depends(get_repository(BankRepository))):
    return Banks(repo)


def get_currency_service(repo: CurrencyRepository = Depends(get_repository(CurrencyRepository))):
    return Currencies(repo)


def get_card_service(repo: CardsRepository = Depends(get_repository(CardsRepository))):
    return Cards(repo)
