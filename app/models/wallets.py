from pydantic import BaseModel


class Wallet(BaseModel):
    user_id: int
    card_id: int
    currency: str
    score: int
    credit_rating: int
    bank: int
