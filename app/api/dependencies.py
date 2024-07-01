from typing import Generator

from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models.common.token_type import TokenType
from app.models.user import User
from app.repositories.comment_gateway import CommentDbGateway
from app.repositories.post_gateway import PostDbGateway
from app.repositories.user_gateway import UserDbGateway
from app.schemas.auth import RefreshToken
from app.schemas.user import UserDTO
from app.services.auth_service import AuthenticationService
from app.services.comment_service import CommentService
from app.services.post_service import PostService
from app.services.user_service import UserService

bearer = HTTPBearer(auto_error=False)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_gateway(db: Session = Depends(get_db)) -> UserDbGateway:
    return UserDbGateway(db)


def get_post_gateway(db: Session = Depends(get_db)) -> PostDbGateway:
    return PostDbGateway(db)


def get_post_service(
    gateway: PostDbGateway = Depends(get_post_gateway),
) -> PostService:
    return PostService(gateway)


def get_comment_gateway(db: Session = Depends(get_db)) -> CommentDbGateway:
    return CommentDbGateway(db)


def get_auth_service(
    gateway: UserDbGateway = Depends(get_user_gateway),
) -> UserDbGateway:
    return AuthenticationService(gateway)


def get_comment_service(
    comment_gateway: CommentDbGateway = Depends(get_comment_gateway),
    post_gateway: PostDbGateway = Depends(get_post_gateway),
) -> CommentService:
    return CommentService(comment_gateway, post_gateway)


def get_user_service(
    gateway: UserDbGateway = Depends(get_user_gateway),
) -> UserService:
    return UserService(gateway)


def get_current_auth_user(
    token: HTTPAuthorizationCredentials = Depends(bearer),
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> UserDTO:
    return auth_service.get_auth_user(token.credentials, TokenType.ACCESS)


def get_current_auth_user_refresh(
    token: RefreshToken,
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> UserDTO:
    return auth_service.get_auth_user(token.refresh_token, TokenType.REFRESH)
