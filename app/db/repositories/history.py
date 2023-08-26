from typing import List

from app.db import BaseRepository
from app.models.common import Id
from app.models.wallets import History


class HistoryRepository(BaseRepository):

    async def add_operation(
            self, wallet_id: int, start_meaning: int, value: int,
            type_operation: int, finish_meaning: int
    ):
        args = (wallet_id, start_meaning, value, type_operation, finish_meaning)
        await self.fetch_one(f"INSERT INTO "
                             f"history_operations(wallet_id, start_meaning, value, type_operation, finish_meaning) "
                             f"VALUES ($1, $2, $3, $4, $5) RETURNING id", *args, serializer=Id)

    async def get_history_by_wallet_id(self, wallet_id: int) -> List[History]:
        result = await self.fetch_rows(f"SELECT value, type_operation "
                                       f"FROM history_operations WHERE wallet_id={wallet_id}", serializer=History)
        return result

