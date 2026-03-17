from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.logs.exceptions import AppError
from src.core.logs.logging import logger


async def app_exception_handler(request: Request, exc: AppError):
    if exc.status_code >= 500:
        level = logger.error
    else:
        level = logger.warning

    level(f"Error on {request.url.path}: {exc.message} | details: {exc.__dict__}")

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "details": exc.__dict__},
    )
