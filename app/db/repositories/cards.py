from datetime import datetime
from typing import List

from app.db import BaseRepository
from app.models.common import Id, Score
from app.models.cards import Card


class CardsRepository(BaseRepository):

    async def insert_card(self, wallet_id: int, user_id: int,
                          card_number: str, expiration_time: datetime, score: int, bank_id: int) -> Card:
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

    async def get_cards_by_user_id(self, user_id: int) -> List[Card]:
        cards = await self.fetch_rows(f"SELECT * FROM cards WHERE user_id={user_id}", serializer=Card)
        return cards
