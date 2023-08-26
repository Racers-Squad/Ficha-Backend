from typing import List

from fastapi import APIRouter, Depends

from app.dependencies.services import get_currency_service
from app.models.currencies import Course, Currency
from app.services.currencies import Currencies

router = APIRouter(tags=["currencies"], prefix="/currencies")


@router.get(
    path="/",
    description="Метод получения списка всех валют",
    response_model=List[Currency]
)
async def get_currencies(
        currency_service: Currencies = Depends(get_currency_service)
):
    result = await currency_service.get_currencies()
    return result


@router.get(
    path="/courses",
    description="Метод получения курсов валют",
    response_model=List[Course]
)
async def get_courses(
        currency_service: Currencies = Depends(get_currency_service)
):
    result = await Currencies.get_currencies_courses()
    return result
