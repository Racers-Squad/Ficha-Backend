from app.db import BaseRepository
from app.models.common import Id
from app.models.users import Users
from loguru import logger



class UserRepository(BaseRepository):
    async def get_user_by_email(self, email: str):
        logger.info(f"Arguments: email - {email}")
        user = await self.fetch_one(f"SELECT * FROM users WHERE email='{email}'", serializer=Users)
        logger.info(f"Response from db: {user}")
        return user

    async def get_admin_rights_by_email(self, email: str) -> int:
        logger.info(f"Arguments: email - {email}")
        rights = await self.fetch_one(f"SELECT role FROM users WHERE email ='{email}'")
        logger.info(f"Response from db: {rights}")
        return rights

    async def insert_user(self,
                          name: str, surname: str, mail: str,
                          password: str, phone: str, role: int) -> int:
        logger.info(f"Arguments: name - {name}, surname - {surname}, mail - {mail}, password - {password}, "
                    f"phone - {phone}, role - {role}")
        args = (name, surname, mail, password, phone, role)
        user = await self.fetch_one(
            "INSERT INTO users(name, surname, email, password, phone, role) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id",
            *args, serializer=Id)
        logger.info(f"Object added to db: {users}")
        return user
