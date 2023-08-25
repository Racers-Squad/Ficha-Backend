from fastapi import APIRouter

from app.api.routes import users, wallets, bank, currencies, cards

router = APIRouter()
router.include_router(users.router)
router.include_router(wallets.router)
router.include_router(bank.router)
router.include_router(currencies.router)
router.include_router(cards.router)
