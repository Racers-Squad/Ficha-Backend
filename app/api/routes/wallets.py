from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.api.errors import USER_NOT_FOUND
from app.dependencies.services import get_wallet_service
from app.models.wallets import WalletCreateRequest
from app.services.wallets import Wallets
from app.utils.exceptions import UserNotFound

router = APIRouter(tags=["wallets"], prefix="/wallets")


@router.get(
    path="/{email}",
    description="Метод получения списка кошельков в email"
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
        result = await wallet_service.create_wallet(body.email, body.bank, body.currency)
        return result
    except UserNotFound:
        return JSONResponse({"error": USER_NOT_FOUND}, status_code=404)
