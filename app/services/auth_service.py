from jose import JWTError

from app.core.exceptions.auth import (
    InvalidCredentials,
    InvalidTokenType,
    NotAuthorized,
    TokenExpired,
)
from app.core.exceptions.entity import UserNotFound
from app.core.security import (
    TOKEN_TYPE_FIELD,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.models.common.token_type import TokenType
from app.repositories.user_gateway import UserDbGateway
from app.schemas.auth import RefreshToken, SignInDTO, TokenInfo
from app.schemas.user import UserDTO


class AuthenticationService:
    def __init__(self, user_gateway: UserDbGateway) -> None:
        self.user_gateway = user_gateway

    def authenticate(self, credentials: SignInDTO) -> TokenInfo:
        user = self.user_gateway.get_by_email(credentials.email)
        if not user:
            raise UserNotFound()
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise InvalidCredentials()
        return self.generate_tokens(user.id)

    def get_auth_user(self, token: str | None, token_type: TokenType) -> UserDTO:
        if not token:
            raise NotAuthorized()
        try:
            payload = decode_token(token)
            if not payload:
                raise TokenExpired()
        except JWTError:
            raise InvalidCredentials()
        if not payload.get(TOKEN_TYPE_FIELD) == token_type:
            raise InvalidTokenType()

        user = self.user_gateway.get_by_id(payload.get("sub"))
        if not user:
            raise UserNotFound()

        return UserDTO.model_validate(user, from_attributes=True)

    def generate_tokens(self, user_id: int, access_only: bool = False) -> TokenInfo:

        return TokenInfo(
            access_token=create_access_token(user_id),
            refresh_token=None if access_only else create_refresh_token(user_id),
            token_type="Bearer",
        )