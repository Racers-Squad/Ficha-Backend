from app.db import BaseRepository
from app.models.common import Id, Score
from app.models.wallets import Wallet
from loguru import logger



class WalletRepository(BaseRepository):
    async def get_wallets_by_user_id(self, user_id: int):
        logger.info(f"Arguments: user_id - {user_id}")
        wallets = await self.fetch_rows(f"SELECT * FROM wallets WHERE user_id={user_id}", serializer=Wallet)
        logger.info(f"Response from db: {wallets}")
        return wallets

    async def insert_wallet(self, user_id: int, currency: int, score: int, status: int) -> int:
        logger.info(f"Arguments: user_id - {user_id}, currency - {currency}, score - {score}, status - {status}")
        args = (user_id, currency, score, status)
        wallet = await self.fetch_one(
            "INSERT INTO wallets(user_id, currency, score, status) VALUES ($1, $2, $3, $4) RETURNING *",
            *args, serializer=Wallet)
        logger.info(f"Object added to db: {wallet}")
        return wallet

    async def get_wallet_by_id(self, wallet_id: int) -> Wallet:
        logger.info(f"Arguments: wallet_id - {wallet_id}")
        wallet = await self.fetch_one(f"SELECT * FROM wallets WHERE id={wallet_id}", serializer=Wallet)
        logger.info(f"Response from db: {wallet}")
        return wallet

    async def change_wallet_score(self, wallet_id: int, money_sum: int) -> Wallet:
        logger.info(f"Arguments: wallet_id - {wallet_id}, money_sum - {money_sum}")
        prev_score = await self.fetch_one(f"SELECT score FROM wallets WHERE id={wallet_id}", serializer=Score)
        logger.info(f"Response from db: {prev_score}")
        result = await self.fetch_one(f"UPDATE wallets SET score={prev_score.score + money_sum}"
                             f" WHERE id={wallet_id} RETURNING *", serializer=Wallet)
        logger.info(f"Object updated in db: {result}")
        return result

    async def get_wallet_score(self,wallet_id: int) -> int:
        logger.info(f"Arguments: wallet_id - {wallet_id}")
        wallet_score = await self.fetch_one(
            f"SELECT score FROM wallets WHERE id ={wallet_id}", serializer=Score)
        logger.info(f"Response from db: {wallet_score}")
        return wallet_score
