from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.errors import CARD_ALREADY_EXISTS
from app.dependencies.services import get_card_service
from app.models.cards import Card
from app.utils.exceptions import CardAlreadyExists

router = APIRouter(tags=["cards"], prefix="/cards")


@router.post(
    path="/add",
    description="Метод создания карты"
)
async def add_card(
        body: Card,
        card_service=Depends(get_card_service)
):
    try:
        result = await card_service.insert_card(body.id, body.wallet_id, body.card_number, body.user_id,
                                                body.expiration_time)
        return result
    except CardAlreadyExists:
        return JSONResponse({"error": CARD_ALREADY_EXISTS}, status_code=404)
