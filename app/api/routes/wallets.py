from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.db import get_repository
from app.db.repositories.user import UserRepository
from app.db.repositories.wallet import WalletRepository

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
