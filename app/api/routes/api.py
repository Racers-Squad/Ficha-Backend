from fastapi import APIRouter

from app.api.routes import users, wallets, bank

router = APIRouter()
router.include_router(users.router)
router.include_router(wallets.router)
router.include_router(bank.router)
