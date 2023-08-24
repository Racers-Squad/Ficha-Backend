import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import jwt

from app.api.errors import USER_ALREADY_EXISTS
from app.config import Config
from app.db import get_repository
from app.db.repositories.user import UserRepository
from app.models.users import RegisterRequest

config = Config()

router = APIRouter(prefix="/users")


@router.post(
    path="/register",
    description="Метод регистрации пользователя"
)
async def register(
        body: RegisterRequest,
        user_repo: UserRepository = Depends(get_repository(UserRepository))
):
    user_exists = await user_repo.get_user_by_email(body.mail)
    if not user_exists:
        payload = {
            "mail": body.mail,
            "name": body.name,
            "surname": body.surname,
            "phone": body.phone,
            "password": body.password,
            "role": body.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        }
        token = jwt.encode(payload, config.app.secret_key, algorithm="HS256")
        await user_repo.insert_user(body.name, body.surname, body.mail, body.password, body.phone, body.role)
        return JSONResponse({"access_token": token})
    else:
        return JSONResponse({"error": USER_ALREADY_EXISTS}, status_code=500)
