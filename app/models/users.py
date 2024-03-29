from pydantic import BaseModel


class Users(BaseModel):
    id: int
    name: str
    surname: str
    mail: str
    password: str
    phone: str
    role: int


class RegisterRequest(BaseModel):
    mail: str
    name: str
    surname: str
    phone: str
    password: str


class LoginRequest(BaseModel):
    mail: str
    password: str


class CheckRequest(BaseModel):
    token: str
