from app.db import BaseRepository
from app.models.common import Id
from app.models.wallets import Wallet


class WalletRepository(BaseRepository):
    async def get_wallets_by_user_id(self, user_id: int):
        wallets = await self.fetch_rows(f"SELECT * FROM wallets WHERE user_id={user_id}", serializer=Wallet)
        return wallets

    async def insert_wallet(self, user_id: int, currency: str, score: int, card_rating: int, bank: int) -> int:
        args = (user_id, currency, score, card_rating, bank)
        wallet = await self.fetch_one(
            "INSERT INTO wallets(user_id, currency, score, card_rating, bank) VALUES ($1, $2, $3, $4, $5) RETURNING card_id",
            *args, serializer=Id)
        return wallet
