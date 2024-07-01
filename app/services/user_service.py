from app.core.exceptions.entity import UserAlreadyExists, UserNotFound
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_gateway import UserDbGateway
from app.schemas.auth import SignUpDTO
from app.schemas.user import UserDTO, UserId


class UserService:
    def __init__(self, user_gateway: UserDbGateway) -> None:
        self.user_gateway = user_gateway

    def create_user(self, dto: SignUpDTO) -> UserDTO:
        if self.user_gateway.get_by_email(dto.email):
            raise UserAlreadyExists("User with this email already exists")
        if self.user_gateway.get_by_username(dto.username):
            raise UserAlreadyExists("User with this username already exists")

        user = User(
            username=dto.username,
            email=dto.email,
            hashed_password=get_password_hash(dto.password),
        )
        self.user_gateway.create(user)
        return UserDTO.model_validate(user, from_attributes=True)

    def get_user(self, dto: UserId) -> UserDTO:
        user = self.user_gateway.get_by_id(dto.user_id)
        if not user:
            raise UserNotFound()

        return UserDTO.model_validate(user, from_attributes=True)
