from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.dependencies.services import get_bank_service
from app.models.banks import Bank
from app.services.banks import Banks

router = APIRouter(tags=["banks"], prefix="/banks")


# TODO Фильтры
@router.get(
    path="/all",
    description="Метод получения списка всех банков",
    response_model=List[Bank]
)
async def get_banks(
        banks_service: Banks = Depends(get_bank_service)
):
    result = await banks_service.get_banks()
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
    return result or JSONResponse({})
