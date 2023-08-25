from pydantic import BaseModel


class Bank(BaseModel):
    id: int
    name: str
    country: str


class Currency(BaseModel):
    id: int
    name: str
    short_name: str
