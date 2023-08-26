from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.api.errors import USER_NOT_FOUND, WALLET_NOT_FOUND
from app.config import Config
from app.dependencies.services import get_wallet_service
from app.models.wallets import WalletCreateRequest, Wallet, FillUpRequest, ChangeRequest
from app.services.wallets import Wallets
from app.utils.exceptions import UserNotFound, WalletNotFound

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
    try:
        result = await wallet_service.get_wallets(email)
        return result or JSONResponse({})
    except UserNotFound:
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)


@router.post(
    path="/add",
    description="Метод добавления нового кошелька"
)
async def create_wallet(
        body: WalletCreateRequest,
        wallet_service: Wallets = Depends(get_wallet_service)
):
    try:
        result = await wallet_service.create_wallet(body.email, body.currency)
        return result
    except UserNotFound:
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
        result = await wallet_service.fill_up_wallet(wallet_id, body.money_sum)
        if result:
            return JSONResponse({})
        else:
            return JSONResponse({"error": "Кошелек не был пополнен"}, status_code=500)
    except WalletNotFound:
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
    try:
        wallets = await wallet_service.change_money(body.sender_wallet_id, body.accept_wallet_id, body.money_sum)
        return wallets
    except WalletNotFound:
        return JSONResponse({"error": WALLET_NOT_FOUND}, status_code=404)

