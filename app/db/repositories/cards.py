from datetime import datetime

from app.db import BaseRepository
from app.models.common import Id, Score
from app.models.cards import Card
from app.models.common import Id


class CardsRepository(BaseRepository):

    async def insert_card(self, wallet_id: int, user_id: int,
                          card_number: int, expiration_time: datetime, score: int, bank_id: int) -> Card:
        args = (wallet_id, user_id, card_number, expiration_time, score, bank_id)
        card = await self.fetch_one(
            "INSERT INTO cards(wallet_id, user_id, card_number, expiration_time, score, bank_id)"
            " VALUES ($1, $2, $3, $4, $5, $6) RETURNING *",
            *args, serializer=Card)
        return card

    async def get_card_score(self,
                             card_number: int) -> int:
        card_score = await self.fetch_one(
            f"SELECT score FROM cards WHERE card_number ={card_number}", serializer=Score)
        return card_score
