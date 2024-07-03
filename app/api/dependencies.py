from typing import AsyncIterator

from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session
from app.models.common.token_type import TokenType
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


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session() as db:
        yield db


async def get_user_gateway(db: AsyncSession = Depends(get_db)) -> UserDbGateway:
    return UserDbGateway(db)


async def get_post_gateway(db: AsyncSession = Depends(get_db)) -> PostDbGateway:
    return PostDbGateway(db)


async def get_post_service(
    gateway: PostDbGateway = Depends(get_post_gateway),
) -> PostService:
    return PostService(gateway)


async def get_comment_gateway(db: AsyncSession = Depends(get_db)) -> CommentDbGateway:
    return CommentDbGateway(db)


async def get_auth_service(
    gateway: UserDbGateway = Depends(get_user_gateway),
) -> AuthenticationService:
    return AuthenticationService(gateway)


async def get_comment_service(
    comment_gateway: CommentDbGateway = Depends(get_comment_gateway),
    post_gateway: PostDbGateway = Depends(get_post_gateway),
) -> CommentService:
    return CommentService(comment_gateway, post_gateway)


async def get_user_service(
    gateway: UserDbGateway = Depends(get_user_gateway),
) -> UserService:
    return UserService(gateway)


async def get_current_auth_user(
    token: HTTPAuthorizationCredentials = Depends(bearer),
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> UserDTO:
    credentials = token.credentials if token else None
    return await auth_service.get_auth_user(credentials, TokenType.ACCESS)


async def get_current_auth_user_refresh(
    token: RefreshToken,
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> UserDTO:
    return await auth_service.get_auth_user(token.refresh_token, TokenType.REFRESH)
