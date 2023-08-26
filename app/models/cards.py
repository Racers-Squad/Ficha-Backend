from datetime import datetime
from datetime import timezone

from pydantic import BaseModel


class CreateCardRequest(BaseModel):
    wallet_id: int
    bank_id: int


class Card(BaseModel):
    id: int
    wallet_id: int
    user_id: int
    card_number: str
    expiration_time: datetime
    score: int
    bank_id: int
