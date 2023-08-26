from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.errors import USER_NOT_FOUND, WALLET_NOT_FOUND, BANK_NOT_FOUND
from app.dependencies.services import get_card_service
from app.models.cards import CreateCardRequest, Card
from app.services.cards import Cards
from app.utils.exceptions import UserNotFound, WalletNotFound, BankNotFound
from loguru import logger

router = APIRouter(tags=["cards"], prefix="/cards")


@router.post(
    path="/{email}/add",
    description="Метод создания карты"
)
async def add_card(
        email: str,
        body: CreateCardRequest,
        card_service: Cards = Depends(get_card_service)
):
    logger.info("Start method add_card")
    try:
        result = await card_service.insert_card(email, body.wallet_id, body.bank_id)
        logger.info("Method get_banks return " + result)
        return result
    except UserNotFound:
        logger.error(f"Method add_card except {USER_NOT_FOUND}")
        logger.info("Finish method add_card")
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)
    except WalletNotFound:
        logger.error(f"Method add_card except {WALLET_NOT_FOUND}")
        logger.info("Finish method add_card")
        return JSONResponse({"error": WALLET_NOT_FOUND}, status_code=404)
    except BankNotFound:
        logger.error(f"Method add_card except {BANK_NOT_FOUND}")
        logger.info("Finish method add_card")
        return JSONResponse({"error": BANK_NOT_FOUND}, status_code=404)


@router.get(
    path="/{email}",
    description="Метод получения всех карточек по имени пользователя",
    response_model=List[Card]
)
async def get_card_by_user(
        email: str,
        card_service: Cards = Depends(get_card_service)
):
    logger.info("Start method get_card_by_user")
    try:
        result = await card_service.get_cards_by_user(email)
        logger.info("Method get_card_by_user return " + result)
        return result
    except UserNotFound:
        logger.error(f"Method get_card_by_user except {USER_NOT_FOUND}")
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)
