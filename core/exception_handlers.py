import logging
from fastapi import Request
from starlette import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from .config import settings

logger = logging.getLogger(__name__)


# 409 error custom handler
def conflict_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder(
            {
                "message": "Database conflict error",
                "detail": str(exc.orig)
            }
        )
    )


# 422 error custom handler
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                "body": exc.body
            }
        )
    )


# 500 error custom handler
def internal_server_error_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error:{exc}", exc_info=True)
    content = {"detail": "Internal server error"}

    if settings.debug:
        content["error"] = str(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(content)
    )
