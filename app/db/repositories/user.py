from app.db import BaseRepository
from app.models.users import Users


class UserRepository(BaseRepository):
    async def get_user_by_email(self, email: str):
        user = await self.fetch_one(f"SELECT * FROM users WHERE mail='{email}'", serializer=Users)
        return user

    async def get_admin_rights_by_email(self, email: str) -> int:
        rights = await self.fetch_one(f"SELECT role FROM users WHERE mail ='{email}'")
        return rights

    async def insert_user(self, name: str,
                          surname: str,
                          mail: str,
                          password: str,
                          phone: str,
                          role: int) -> int:
        args = (name, surname, mail, password, phone, role)
        user_id = await self.fetch_one(
            "INSERT INTO user(name, surname, mail, password, phone, role) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id",
            *args, )
        return user_id
