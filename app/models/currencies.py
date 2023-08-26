from pydantic import BaseModel


class Currency(BaseModel):
    id: int
    name: str
    short_name: str


class Course(BaseModel):
    short_name: str
    course: float
