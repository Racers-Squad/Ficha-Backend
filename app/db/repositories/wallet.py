from app.db import BaseRepository
from app.models.common import Id, Score
from app.models.wallets import Wallet


class WalletRepository(BaseRepository):
    async def get_wallets_by_user_id(self, user_id: int):
        wallets = await self.fetch_rows(f"SELECT * FROM wallets WHERE user_id={user_id}", serializer=Wallet)
        return wallets

    async def insert_wallet(self, user_id: int, currency: int, score: int, status: int) -> int:
        args = (user_id, currency, score, status)
        wallet = await self.fetch_one(
            "INSERT INTO wallets(user_id, currency, score, status) VALUES ($1, $2, $3, $4) RETURNING *",
            *args, serializer=Wallet)
        print(wallet)
        return wallet

    async def get_wallet_by_id(self, wallet_id: int) -> Wallet:
        wallet = await self.fetch_one(f"SELECT * FROM wallets WHERE id={wallet_id}", serializer=Wallet)
        return wallet

    async def change_wallet_score(self, wallet_id: int, money_sum: int):
        prev_score = await self.fetch_one(f"SELECT score FROM wallets WHERE id={wallet_id}", serializer=Score)
        await self.fetch_one(f"UPDATE wallets SET score={prev_score.score + money_sum} WHERE id={wallet_id}")
