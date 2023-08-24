from fastapi.requests import Request
from fastapi.responses import JSONResponse
from loguru import logger

from app.db import SQLException


async def db_error_handler(_: Request, e: SQLException) -> JSONResponse:
    logger.error(e)
    return JSONResponse(status_code=500, content={'reason': str(e)})
