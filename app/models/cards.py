from datetime import datetime

from pydantic import BaseModel

class Card(BaseModel):
    id: int
    wallet_id: int
    user_id: int
    card_number: int
    expiration_time: datetime

