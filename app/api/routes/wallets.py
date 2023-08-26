from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.api.errors import USER_NOT_FOUND, WALLET_NOT_FOUND, CARD_NOT_FOUND, NOT_ENOUGH_MONEY
from app.config import Config
from app.dependencies.services import get_wallet_service
from app.models.wallets import WalletCreateRequest, Wallet, FillUpRequest, ChangeRequest, WithdrawRequest, History
from app.services.wallets import Wallets
from app.utils.exceptions import UserNotFound, WalletNotFound
from loguru import logger
from app.utils.exceptions import UserNotFound, WalletNotFound, CardNotFound, NotEnoughMoney

config = Config()

router = APIRouter(tags=["wallets"], prefix="/wallets")


@router.get(
    path="/{email}",
    description="Метод получения списка кошельков в email",
    response_model=List[Wallet]
)
async def get_wallets(
        email: str,
        wallet_service: Wallets = Depends(get_wallet_service)
):
    logger.info("Start method get_wallets")
    try:
        result = await wallet_service.get_wallets(email)
        logger.info("Method get_wallets return " + result)
        logger.info("Finish method get_wallets")
        return result or JSONResponse({})
    except UserNotFound:
        logger.error(f"Method get_wallets except {USER_NOT_FOUND}")
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)


@router.post(
    path="/add",
    description="Метод добавления нового кошелька"
)
async def create_wallet(
        body: WalletCreateRequest,
        wallet_service: Wallets = Depends(get_wallet_service)
):
    logger.info("Start method create_wallet")
    try:
        result = await wallet_service.create_wallet(body.email, body.currency)
        logger.info("Method create_wallet return " + result)
        logger.info("Finish method create_wallet")
        return result
    except UserNotFound:
        logger.error(f"Method create_wallet except {USER_NOT_FOUND}")
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)


@router.post(
    path="/{wallet_id}/replenishment",
    description="Метод пополнения кошелька"
)
async def fill_up_wallet(
        wallet_id: int,
        body: FillUpRequest,
        wallet_service: Wallets = Depends(get_wallet_service)
):
    try:
        logger.info("Start method fill_up_wallet")
        result = await wallet_service.fill_up_wallet(wallet_id, body.money_sum)
        if result:
            logger.info("Finish method fill_up_wallet")
            return JSONResponse({})
        else:
            logger.error(f"Method fill_up_wallet except Кошелек не был пополнен")
            return JSONResponse({"error": "Кошелек не был пополнен"}, status_code=500)
    except WalletNotFound:
        logger.error(f"Method fill_up_wallet except {WALLET_NOT_FOUND}")
        return JSONResponse({"error": WALLET_NOT_FOUND}, status_code=404)


@router.post(
    path="/change",
    description="Метод для обмена валют между кошельками",
    response_model=List[Wallet]
)
async def change_money(
        body: ChangeRequest,
        wallet_service: Wallets = Depends(get_wallet_service)
):
    logger.info("Start method change_money")
    try:
        wallets = await wallet_service.change_money(body.sender_wallet_id, body.accept_wallet_id, body.money_sum)
        logger.info("Method change_money return " + wallets)
        logger.info("Finish method change_money")
        return wallets
    except WalletNotFound:
        logger.error(f"Method change_money except {WALLET_NOT_FOUND}")
        return JSONResponse({"error": WALLET_NOT_FOUND}, status_code=404)
    except NotEnoughMoney:
        logger.error(f"Method change_money except {NOT_ENOUGH_MONEY}")
        return JSONResponse({"error": NOT_ENOUGH_MONEY}, status_code=500)


@router.post(
    path="/{wallet_id}/withdraw",
    description="Метод перевода денег с кошелька на карту"
)
async def withdraw_to_card(
        wallet_id: int,
        body: WithdrawRequest,
        wallet_service: Wallets = Depends(get_wallet_service)
):
    logger.info("Start method withdraw_to_card")
    try:
        result = await wallet_service.withdraw_to_card(wallet_id, body.card_number, body.money_sum)
        logger.info("Method withdraw_to_card return " + result)
        logger.info("Finish method withdraw_to_card")
        return result
    except WalletNotFound:
        logger.error(f"Method withdraw_to_card except {WALLET_NOT_FOUND}")
        return JSONResponse({"error": WALLET_NOT_FOUND}, status_code=404)
    except CardNotFound:
        logger.error(f"Method withdraw_to_card except {CARD_NOT_FOUND}")
        return JSONResponse({"error": CARD_NOT_FOUND}, status_code=404)
    except NotEnoughMoney:
        logger.error(f"Method withdraw_to_card except {NOT_ENOUGH_MONEY}")
        return JSONResponse({"error": NOT_ENOUGH_MONEY}, status_code=500)


@router.get(
    path="/{wallet_id}/history",
    description="Метод получения истории кошелька",
    response_model=List[History]
)
async def get_wallet_history(
        wallet_id: int,
        wallet_service: Wallets = Depends(get_wallet_service)
):
    logger.info("Start method get_wallet_history")
    try:
        result = await wallet_service.get_wallet_history(wallet_id)
        logger.info("Method get_wallet_history return " + result)
        logger.info("Finish method get_wallet_history")
        return result
    except WalletNotFound:
        logger.error(f"Method get_wallet_history except {WALLET_NOT_FOUND}")
        return JSONResponse({"error": WALLET_NOT_FOUND}, status_code=404)
