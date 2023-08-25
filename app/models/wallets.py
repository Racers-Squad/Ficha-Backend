from pydantic import BaseModel


class Wallet(BaseModel):
    user_id: int
    id: int
    currency: int
    score: int
    status: int


class WalletCreateRequest(BaseModel):
    currency: int
    email: str


class FillUpRequest(BaseModel):
    money_sum: int
    card_number: int
