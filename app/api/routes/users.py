import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import jwt

from app.api.errors import USER_ALREADY_EXISTS, PASSWORD_INCORRECT, USER_NOT_FOUND
from app.config import Config
from app.db import get_repository
from app.db.repositories.user import UserRepository
from app.models.users import RegisterRequest, LoginRequest

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
        return JSONResponse({"access_token": token})
    else:
        return JSONResponse({"error": USER_ALREADY_EXISTS}, status_code=500)


@router.post(
    path="/login",
    description="Логин"
)
async def login(
        body: LoginRequest,
        user_repo: UserRepository = Depends(get_repository(UserRepository))
):
    user_exists = await user_repo.get_user_by_email(body.mail)
    if user_exists:
        if user_exists.password == body.password:
            payload = {
                "mail": body.mail,
                "password": body.password,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            }
            token = jwt.encode(payload, config.app.secret_key, algorithm="HS256")
            return JSONResponse({"access_token": token})
        else:
            return JSONResponse({"error": PASSWORD_INCORRECT}, status_code=500)
    else:
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)



