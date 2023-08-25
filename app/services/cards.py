from datetime import datetime

from app.db.repositories.cards import CardsRepository


class Cards:

    def __init__(self, repo):
        self.repo: CardsRepository = repo

    async def insert_card(self, wallet_id: int, user_id: int, card_number: int, expiration_time: datetime):
        result = await self.repo.insert_card(wallet_id, user_id, card_number, expiration_time)
        return result
