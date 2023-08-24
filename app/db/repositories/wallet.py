from app.db import BaseRepository
from app.models.wallets import Wallet


class WalletRepository(BaseRepository):
    async def get_wallets_by_user_id(self, user_id: int):
        wallets = await self.fetch_rows(f"SELECT * FROM wallets WHERE user_id={user_id}", serializer=Wallet)
        return wallets
