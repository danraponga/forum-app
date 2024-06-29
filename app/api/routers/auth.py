from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import (
    get_current_auth_user,
    get_current_auth_user_refresh,
    get_user_gateway,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.user import User
from app.repositories.user_gateway import UserDbGateway
from app.schemas.auth import SignInDTO, SignUpDTO, SignUpResultDTO, TokenInfo
from app.schemas.user import UserDTO

auth_router = APIRouter()


@auth_router.post("/sign_up", response_model=UserDTO)
def sign_up(
    user_data: SignUpDTO,
    user_gateway: UserDbGateway = Depends(get_user_gateway),
) -> SignUpResultDTO:
    if user_gateway.get_by_email(user_data.email):
        raise HTTPException(status_code=409, detail="User already exists")

    user = User(**user_data)
    user_gateway.create(user)

    return SignUpResultDTO(
        user=UserDTO.model_validate(user, from_attributes=True),
        tokens=TokenInfo(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        ),
    )


@auth_router.post("/login")
def sign_in(
    credentials: SignInDTO,
    user_gateway: UserDbGateway = Depends(get_user_gateway),
) -> TokenInfo:
    user = user_gateway.get_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenInfo(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@auth_router.get("/me", response_model=UserDTO)
def me(user: User = Depends(get_current_auth_user)) -> User:
    return user


@auth_router.post("/refresh", response_model_exclude_none=True)
def refresh_access_token(
    user: User = Depends(get_current_auth_user_refresh),
) -> TokenInfo:
    return TokenInfo(access_token=create_access_token(user.id))
