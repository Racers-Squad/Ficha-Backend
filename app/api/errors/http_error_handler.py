from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from loguru import logger


async def http_error_handler(_: Request, e: HTTPException) -> JSONResponse:
    logger.info(e)
    return JSONResponse({
        "errors": [
            e.detail
        ]
    }, status_code=e.status_code)
