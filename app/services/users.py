import datetime
from typing import Optional

import jwt

from app.config import Config
from app.db.repositories.user import UserRepository
from app.utils.exceptions import PasswordIncorrect, UserNotFound

config = Config()


class Users:

    def __init__(self, repo):
        self.repo: UserRepository = repo

    async def register(
            self,
            mail: str, name: str, surname: str, phone: str, password: str, role: int
    ) -> Optional[str]:
        user_exists = await self.repo.get_user_by_email(mail)
        if not user_exists:
            payload = {
                "mail": mail,
                "name": name,
                "surname": surname,
                "phone": phone,
                "password": password,
                "role": role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            }
            token = jwt.encode(payload, config.app.secret_key, algorithm="HS256")
            await self.repo.insert_user(name, surname, mail, password, phone, role)
            return token
        else:
            return None

    async def login(
            self,
            email: str, password: str
    ):
        user_exists = await self.repo.get_user_by_email(email)
        if user_exists:
            if user_exists.password == password:
                payload = {
                    "mail": email,
                    "password": password,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                }
                token = jwt.encode(payload, config.app.secret_key, algorithm="HS256")
                return token
            else:
                raise PasswordIncorrect
        else:
            raise UserNotFound

    async def token_check(
            self,
            token: str
    ):
        user_check = jwt.decode(token, config.app.secret_key, algorithms="HS256")
        user = await self.repo.get_user_by_email(user_check.get('mail'))
        if not user:
            raise UserNotFound
        else:
            if user.password == user_check.get('password'):
                return jwt.encode({
                    "mail": user.mail,
                    "name": user.name,
                    "surname": user.surname,
                    "phone": user.phone,
                    "password": user.password,
                    "role": user.role,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                }, config.app.secret_key, algorithm="HS256")
            else:
                raise PasswordIncorrect
