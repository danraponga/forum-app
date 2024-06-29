from pydantic import BaseModel, EmailStr

from app.schemas.user import UserDTO


class RefreshToken(BaseModel):
    refresh_token: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str | None = "Bearer"


class SignUpDTO(BaseModel):
    username: str
    email: EmailStr
    password: str


class SignUpResultDTO(BaseModel):
    user: UserDTO
    tokens: TokenInfo


class SignInDTO(BaseModel):
    email: EmailStr
    password: str
