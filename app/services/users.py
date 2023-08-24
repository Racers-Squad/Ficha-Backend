import datetime
from typing import Optional

import jwt

from app.db.repositories.user import UserRepository
from app.main import config
from app.utils.exceptions import PasswordIncorrect, UserNotFound


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

