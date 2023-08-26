from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from app.api.errors import BANK_NOT_FOUND
from app.dependencies.services import get_bank_service
from app.models.banks import Bank
from app.models.currencies import Currency
from app.services.banks import Banks
from app.utils.exceptions import BankNotFound
from loguru import logger

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
    logger.info("Start method get_banks")
    result = await banks_service.get_banks(currency_id)
    logger.info("Method get_banks return " + result)
    logger.info("Finish method get_banks")
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
    logger.info("Start method get_bank_by_id")
    result = await bank_service.get_bank_by_id(bank_id)
    if result:
        logger.info("Method get_bank_by_id return " + result)
    else:
        logger.error(f"Method get_bank_by_id except {BANK_NOT_FOUND}")
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
    logger.info("Start method get_bank_by_id")
    try:
        result = await bank_service.get_bank_currencies(bank_id)
        logger.info("Method get_bank_currencies return " + result)
        return result
    except BankNotFound:
        logger.error(f"Method get_bank_currencies except {BANK_NOT_FOUND}")
        return JSONResponse({"error": BANK_NOT_FOUND}, status_code=404)
