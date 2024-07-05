from fastapi import FastAPI
from pydantic import ValidationError

from app.api.exception_handler import (
    access_denied_error_handler,
    authentication_error_handler,
    entity_not_found_error_handler,
    profanity_content_error_handler,
    user_already_exists_handler,
    validation_error_handler,
)
from app.core.exceptions.auth import AuthenticationError
from app.core.exceptions.common import AccessDenied, ProfanityContent
from app.core.exceptions.entity import EntityNotFoundError, UserAlreadyExists


def init_exception_handlers(app: FastAPI):
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(AccessDenied, access_denied_error_handler)
    app.add_exception_handler(ProfanityContent, profanity_content_error_handler)
    app.add_exception_handler(EntityNotFoundError, entity_not_found_error_handler)
    app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
