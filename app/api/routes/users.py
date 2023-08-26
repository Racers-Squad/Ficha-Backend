from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.errors import USER_ALREADY_EXISTS, PASSWORD_INCORRECT, USER_NOT_FOUND
from app.config import Config
from app.dependencies.services import get_user_service
from app.models.users import RegisterRequest, LoginRequest, CheckRequest
from app.services.users import Users
from app.utils.exceptions import PasswordIncorrect, UserNotFound
from loguru import logger

config = Config()

router = APIRouter(tags=["users"], prefix="/users")


@router.post(
    path="/register",
    description="Метод регистрации пользователя"
)
async def register(
        body: RegisterRequest,
        user_service: Users = Depends(get_user_service)
):
    logger.info("Start method register")
    result = await user_service.register(body.mail, body.name, body.surname, body.phone, body.password, 0)
    if result:
        logger.info("Method register return " + result)
        logger.info("Finish method register")
        return JSONResponse({"access_token": result})
    else:
        logger.error(f"Method register except {USER_ALREADY_EXISTS}")
        return JSONResponse({"error": USER_ALREADY_EXISTS}, status_code=500)


@router.post(
    path="/login",
    description="Метод авторизации пользователя"
)
async def login(
        body: LoginRequest,
        user_service: Users = Depends(get_user_service)
):
    logger.info("Start method login")
    try:
        result = await user_service.login(body.mail, body.password)
        logger.info("Method login return " + result)
        logger.info("Finish method login")
        return JSONResponse({"access_token": result})
    except PasswordIncorrect:
        logger.error(f"Method login except {PASSWORD_INCORRECT}")
        return JSONResponse({"error": PASSWORD_INCORRECT}, status_code=500)
    except UserNotFound:
        logger.error(f"Method login except {USER_NOT_FOUND}")
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)


@router.post(
    path="/check",
    description="Проверка токена"
)
async def check_token(
        body: CheckRequest,
        user_service: Users = Depends(get_user_service)
):
    logger.info("Start method check_token")
    try:
        result = await user_service.token_check(body.token)
        logger.info("Method check_token return " + result)
        logger.info("Finish method check_token")
        return JSONResponse({"access_token": result})
    except UserNotFound:
        logger.error(f"Method check_token except {USER_NOT_FOUND}")
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)
    except PasswordIncorrect:
        logger.error(f"Method check_token except {PASSWORD_INCORRECT}")
        return JSONResponse({"error": PASSWORD_INCORRECT}, status_code=500)
