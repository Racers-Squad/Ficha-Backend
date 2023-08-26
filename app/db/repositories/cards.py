from datetime import datetime
from typing import List

from app.db import BaseRepository
from app.models.common import Id, Score
from app.models.cards import Card
from loguru import logger


class CardsRepository(BaseRepository):

    async def insert_card(self, wallet_id: int, user_id: int,
                          card_number: str, expiration_time: datetime, score: int, bank_id: int) -> Card:
        logger.info(f"Arguments: wallet_id - {wallet_id}, user_id - {user_id}, card_number - {card_number},"
                    f" expiration_time - {expiration_time}, score - {score}, bank_id - {bank_id}")
        args = (wallet_id, user_id, card_number, expiration_time, score, bank_id)
        card = await self.fetch_one(
            "INSERT INTO cards(wallet_id, user_id, card_number, expiration_time, score, bank_id)"
            " VALUES ($1, $2, $3, $4, $5, $6) RETURNING *",
            *args, serializer=Card)
        logger.info(f"Response from db: {card}")
        return card

    async def get_card_score(self,
                             card_number: int) -> int:
        logger.info(f"Arguments: card_number - {card_number}")
        card_score = await self.fetch_one(
            f"SELECT score FROM cards WHERE card_number ={card_number}", serializer=Score)
        logger.info(f"Response from db: {card_score}")
        return card_score

    async def get_cards_by_user_id(self, user_id: int) -> List[Card]:
        logger.info(f"Arguments: user_id - {user_id}")
        cards = await self.fetch_rows(f"SELECT * FROM cards WHERE user_id={user_id}", serializer=Card)
        logger.info(f"Response from db: {cards}")
        return cards
