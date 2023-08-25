from pydantic import BaseModel


class Id(BaseModel):
    id: int


class Score(BaseModel):
    score: int
