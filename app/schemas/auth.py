from pydantic import BaseModel, EmailStr, Field, model_validator

from app.schemas.user import UserDTO


class RefreshToken(BaseModel):
    refresh_token: str = Field(examples=["Your content here"])


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str | None = "Bearer"


class SignUpDTO(BaseModel):
    username: str = Field(min_length=4, max_length=16, examples=["username"])
    email: EmailStr
    password: str = Field(min_length=4, examples=["securepassword1"])

    @model_validator(mode="before")
    @classmethod
    def validate_password(cls, data: dict) -> dict:
        if not any(char.isdigit() for char in data["password"]):
            raise ValueError("Password must contain at least one number")
        return data


class SignUpResultDTO(BaseModel):
    user: UserDTO
    tokens: TokenInfo


class SignInDTO(BaseModel):
    email: EmailStr
    password: str = Field(examples=["securepassword1"])
