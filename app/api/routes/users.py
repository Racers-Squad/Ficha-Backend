from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.errors import USER_ALREADY_EXISTS, PASSWORD_INCORRECT, USER_NOT_FOUND
from app.config import Config
from app.dependencies.services import get_user_service
from app.models.users import RegisterRequest, LoginRequest
from app.services.users import Users
from app.utils.exceptions import PasswordIncorrect, UserNotFound

config = Config()

router = APIRouter(prefix="/users")


@router.post(
    path="/register",
    description="Метод регистрации пользователя"
)
async def register(
        body: RegisterRequest,
        user_service: Users = Depends(get_user_service)
):
    result = await user_service.register(body.mail, body.name, body.surname, body.phone, body.password, body.role)
    if result:
        return JSONResponse({"access_token": result})
    else:
        return JSONResponse({"error": USER_ALREADY_EXISTS}, status_code=500)


@router.post(
    path="/login",
    description="Логин"
)
async def login(
        body: LoginRequest,
        user_service: Users = Depends(get_user_service)
):
    try:
        result = user_service.login(body.mail, body.password)
        return JSONResponse({"access_token": result})
    except PasswordIncorrect:
        return JSONResponse({"error": PASSWORD_INCORRECT}, status_code=500)
    except UserNotFound:
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)



