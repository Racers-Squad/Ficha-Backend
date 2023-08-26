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
    sender_wallet_id: int
    accept_wallet_id: int
    money_sum: int


class WithdrawRequest(BaseModel):
    card_number: str
    money_sum: int


class History(BaseModel):
    value: int
    type_operation: int
