from pydantic import BaseModel


class Users(BaseModel):
    id: int
    name: str
    surname: str
    mail: str
    password: str
    phone: str
    role: int
