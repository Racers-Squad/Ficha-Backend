from datetime import datetime

from app.db import BaseRepository
from app.models.common import Id


class CardsRepository(BaseRepository):

    async def insert_card(self, wallet_id: int, user_id: int, card_number: int, expiration_time: datetime) -> int:
        score = 0
        args = (wallet_id, user_id, card_number, expiration_time, score)
        card = await self.fetch_one(
            "INSERT INTO cards(wallet_id, user_id, card_number, expiration_time) VALUES ($1, $2, $3, $4, $5) RETURNING id",
            *args, serializer=Id)
        return card
