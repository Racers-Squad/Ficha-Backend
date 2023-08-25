from datetime import datetime

from pydantic import BaseModel


class CreateCardRequest(BaseModel):
    id: int
    wallet_id: int
    user_id: int
    card_number: int
    expiration_time: datetime
