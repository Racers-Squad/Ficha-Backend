from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.errors import CARD_ALREADY_EXISTS
from app.dependencies.services import get_card_service
from app.models.cards import CreateCardRequest
from app.services.cards import Cards
from app.utils.exceptions import CardAlreadyExists

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
    try:
        result = await card_service.insert_card(body.id, body.wallet_id, body.card_number, body.user_id,
                                                body.expiration_time)
        return result
    except CardAlreadyExists:
        return JSONResponse({"error": CARD_ALREADY_EXISTS}, status_code=500)
