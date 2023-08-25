from fastapi import Depends

from app.db.repositories.user import UserRepository
from app.db.repositories.wallet import WalletRepository
from app.dependencies.db import get_repository
from app.services.users import Users
from app.services.wallets import Wallets


def get_user_service(repo: UserRepository = Depends(get_repository(UserRepository))):
    return Users(repo)


def get_wallet_service(repo: WalletRepository = Depends(get_repository(WalletRepository)),
                       user_service: UserRepository = Depends(get_repository(UserRepository))):
    return Wallets(repo, user_service)
