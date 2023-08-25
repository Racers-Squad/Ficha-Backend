from app.db.repositories.user import UserRepository
from app.db.repositories.wallet import WalletRepository
from app.services.users import Users
from app.utils.exceptions import UserNotFound


class Wallets:

    def __init__(self, repo, user_repo):
        self.repo: WalletRepository = repo
        self.user_repo: UserRepository = user_repo

    async def get_wallets(self, email: str):
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFound
        wallets = await self.repo.get_wallets_by_user_id(user.id)
        return wallets or None

    async def create_wallet(self, email: str, bank: int, currency: str):
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFound
        wallet_id = await self.repo.insert_wallet(user.id, currency, 0, 0, bank)
        return wallet_id
