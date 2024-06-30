from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserDTO


class RefreshToken(BaseModel):
    refresh_token: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str | None = "Bearer"


class SignUpDTO(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(min_length=4)


class SignUpResultDTO(BaseModel):
    user: UserDTO
    tokens: TokenInfo


class SignInDTO(BaseModel):
    email: EmailStr
    password: str
