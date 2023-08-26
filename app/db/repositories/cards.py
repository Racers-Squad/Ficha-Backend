from datetime import datetime
from typing import List

from app.db import BaseRepository
from app.models.common import Id, Score
from app.models.cards import Card


class CardRepository(BaseRepository):

    async def insert_card(self, wallet_id: int, user_id: int,
                          card_number: str, expiration_time: datetime, score: int, bank_id: int) -> Card:
        args = (wallet_id, user_id, card_number, expiration_time, score, bank_id)
        card = await self.fetch_one(
            "INSERT INTO cards(wallet_id, user_id, card_number, expiration_time, score, bank_id)"
            " VALUES ($1, $2, $3, $4, $5, $6) RETURNING *",
            *args, serializer=Card)
        return card

    async def get_card_score(self,
                             card_number: str) -> int:
        card_score = await self.fetch_one(
            f"SELECT score FROM cards WHERE card_number ='{card_number}'", serializer=Score)
        return card_score

    async def get_cards_by_user_id(self, user_id: int) -> List[Card]:
        cards = await self.fetch_rows(f"SELECT * FROM cards WHERE user_id={user_id}", serializer=Card)
        return cards

    async def get_card_by_card_number(self, card_number: str) -> Card:
        card = await self.fetch_one(f"SELECT * FROM cards WHERE card_number='{card_number}'", serializer=Card)
        return card

    async def change_card_balance_by_card_number(self, card_number: str, money_sum: int):
        prev_score = await self.fetch_one(f"SELECT score FROM cards WHERE card_number='{card_number}'", serializer=Score)
        card = await self.fetch_one(f"UPDATE cards SET score={prev_score.score + money_sum} "
                                    f"WHERE card_number='{card_number}' returning *", serializer=Card)
        return card
