from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.exceptions.auth import AuthenticationError
from app.core.exceptions.common import AccessDenied, ProfanityContent
from app.core.exceptions.entity import EntityNotFoundError, UserAlreadyExists


async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


async def authentication_error_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(status_code=401, content={"detail": exc.detail})


async def access_denied_error_handler(request: Request, exc: AccessDenied):
    return JSONResponse(status_code=403, content={"detail": exc.detail})


async def profanity_content_error_handler(request: Request, exc: ProfanityContent):
    return JSONResponse(status_code=400, content={"detail": exc.detail})


async def entity_not_found_error_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.detail})


async def user_already_exists_handler(request: Request, exc: UserAlreadyExists):
    return JSONResponse(status_code=409, content={"detail": exc.detail})
