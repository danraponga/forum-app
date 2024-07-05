from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_auth_service,
    get_current_auth_user,
    get_current_auth_user_refresh,
    get_user_service,
)
from app.schemas.auth import SignInDTO, SignUpDTO, SignUpResultDTO, TokenInfo
from app.schemas.user import UserDTO
from app.services.auth_service import AuthenticationService
from app.services.user_service import UserService

auth_router = APIRouter()


@auth_router.post("/sign_up/")
async def sign_up(
    user_data: SignUpDTO,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> SignUpResultDTO:
    user = await user_service.create_user(user_data)
    tokens = auth_service.generate_tokens(user.id)
    return SignUpResultDTO(user=user, tokens=tokens)


@auth_router.post("/login/")
async def sign_in(
    credentials: SignInDTO,
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> TokenInfo:
    return await auth_service.authenticate(credentials)


@auth_router.get("/me/", response_model=UserDTO)
async def me(user: UserDTO = Depends(get_current_auth_user)) -> UserDTO:
    return user


@auth_router.post("/refresh/", response_model_exclude_none=True)
async def refresh_access_token(
    user: UserDTO = Depends(get_current_auth_user_refresh),
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> TokenInfo:
    return auth_service.generate_tokens(user.id, access_only=True)
