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


class ChangeRequest(BaseModel):
    wallet_id_1: int
    wallet_id_2: int
    money_sum: int
