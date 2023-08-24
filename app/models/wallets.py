from pydantic import BaseModel


class Wallets(BaseModel):
    user_id: int
    card_id: int
    currency: str
    score: int
    credit_rating: int
    bank: int