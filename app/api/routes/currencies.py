from typing import List

from fastapi import APIRouter, Depends

from app.dependencies.services import get_currency_service
from app.models.banks import Currency
from app.services.currencies import Currencies
from loguru import logger

router = APIRouter(tags=["currencies"], prefix="/currencies")


@router.get(
    path="/",
    description="Метод получения списка всех валют",
    response_model=List[Currency]
)
async def get_currencies(
        currency_service: Currencies = Depends(get_currency_service)
):
    logger.info("Start method get_currencies")
    result = await currency_service.get_currencies()
    logger.info("Method get_currencies return " + result)
    logger.info("Finish method get_currencies")
    return result
