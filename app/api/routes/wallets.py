from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.db.repositories.user import UserRepository
from app.db.repositories.wallet import WalletRepository
from app.dependencies.db import get_repository
from app.models.wallets import WalletCreateRequest

router = APIRouter(prefix="/wallets")


@router.get(
    path="/{email}",
    description=""
)
async def get_wallets(
        email: str,
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        wallets_repo: WalletRepository = Depends(get_repository(WalletRepository))
):
    user = await user_repo.get_user_by_email(email)
    wallets = await wallets_repo.get_wallets_by_user_id(user.id)
    if not wallets:
        return JSONResponse({})
    else:
        return wallets


@router.post(
    path="/add",
    description=""
)
async def insert_wallets(
        body: WalletCreateRequest,
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        wallets_repo: WalletRepository = Depends(get_repository(WalletRepository))
):
    user = await user_repo.get_user_by_email(body.email)
    result = await wallets_repo.insert_wallet(user.user_id, body.currency, 0, 0, body.bank)
    return JSONResponse({})
