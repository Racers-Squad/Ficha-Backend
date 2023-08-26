from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from app.api.errors import BANK_NOT_FOUND
from app.dependencies.services import get_bank_service
from app.models.banks import Bank, Currency
from app.services.banks import Banks
from app.utils.exceptions import BankNotFound

router = APIRouter(tags=["banks"], prefix="/banks")


@router.get(
    path="/all",
    description="Метод получения списка всех банков",
    response_model=List[Bank]
)
async def get_banks(
        currency_id: Optional[int] = Query(default=None),
        banks_service: Banks = Depends(get_bank_service)
):
    result = await banks_service.get_banks(currency_id)
    return result or JSONResponse({})


@router.get(
    path="/{bank_id}",
    description="Метод получения банка по id",
    response_model=Bank
)
async def get_bank_by_id(
        bank_id: int,
        bank_service: Banks = Depends(get_bank_service)
):
    result = await bank_service.get_bank_by_id(bank_id)
    return result or JSONResponse({"error": BANK_NOT_FOUND}, status_code=404)


@router.get(
    path="/{bank_id}/currencies",
    description="Метод дял получения валют банка",
    response_model=List[Currency]
)
async def get_bank_currencies(
        bank_id: int,
        bank_service: Banks = Depends(get_bank_service)
):
    try:
        result = await bank_service.get_bank_currencies(bank_id)
        return result
    except BankNotFound:
        return JSONResponse({"error": BANK_NOT_FOUND}, status_code=404)
