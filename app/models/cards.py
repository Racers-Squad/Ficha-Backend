from datetime import datetime

from pydantic import BaseModel


class CreateCardRequest(BaseModel):
    wallet_id: int
    bank_id: int
