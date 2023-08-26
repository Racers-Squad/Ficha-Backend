from app.db import BaseRepository
from app.models.common import Id
from loguru import logger



class HistoryRepository(BaseRepository):

    async def add_operation(
            self, wallet_id: int, start_meaning: int, value: int,
            type_operation: int, finish_meaning: int
    ):
        logger.info(f"Arguments: wallet_id - {wallet_id}, start_meaning - {start_meaning}, value - {value},"
                    f" type_operation - {type_operation}, finish_meaning - {finish_meaning}")
        args = (wallet_id, start_meaning, value, type_operation, finish_meaning)
        await self.fetch_one(f"INSERT INTO "
                             f"history_operations(wallet_id, start_meaning, value, type_operation, finish_meaning) "
                             f"VALUES ($1, $2, $3, $4, $5) RETURNING id", *args, serializer=Id)
        logger.info(f"Object added to db history_operations")

