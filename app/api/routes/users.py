import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import jwt

from app.api.errors import USER_ALREADY_EXISTS, PASSWORD_INCORRECT, USER_NOT_FOUND
from app.config import Config
from app.db import get_repository
from app.db.repositories.user import UserRepository
from app.models.users import RegisterRequest, LoginRequest, CheckRequest

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
                "name": user_exists.name,
                "surname": user_exists.surname,
                "phone": user_exists.phone,
                "password": body.password,
                "role": user_exists.role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            }
            token = jwt.encode(payload, config.app.secret_key, algorithm="HS256")
            return JSONResponse({"access_token": token})
        else:
            return JSONResponse({"error": PASSWORD_INCORRECT}, status_code=500)
    else:
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)


@router.post(
    path="/check",
    description="Проверка токена"
)
async def check_token(
        body: CheckRequest,
        user_repo: UserRepository = Depends(get_repository(UserRepository))
):
    if body != "":
        user_check = jwt.decode(body.token, config.app.secret_key, algorithms="HS256")
        user = await user_repo.get_user_by_email(user_check.get('mail'))
        if not user:
            return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)
        else:
            if user.password == user_check.get('password'):
                return JSONResponse({"access_token": jwt.encode({
                    "mail": user.mail,
                    "name": user.name,
                    "surname": user.surname,
                    "phone": user.phone,
                    "password": user.password,
                    "role": user.role,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                }, config.app.secret_key, algorithm="HS256")})
            else:
                return JSONResponse({"error": PASSWORD_INCORRECT}, status_code=500)
