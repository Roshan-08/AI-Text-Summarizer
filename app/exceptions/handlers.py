import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled application exception | path=%s | method=%s",
        request.url.path,
        request.method
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An internal server error occurred.",
            "error_code": "INTERNAL_SERVER_ERROR",
            "data": None
        }
    )