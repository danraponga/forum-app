from fastapi import APIRouter, Depends

from app.api.dependencies import get_user_gateway, get_user_service
from app.repositories.user_gateway import UserDbGateway
from app.schemas.pagination import Pagination
from app.schemas.user import UserDTO, UserId, UsersListResultDTO
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.get("/")
async def read_users_all(
    pagination: Pagination = Depends(),
    user_gateway: UserDbGateway = Depends(get_user_gateway),
) -> UsersListResultDTO:
    users, total = await user_gateway.get_list(pagination.skip, pagination.limit)
    users_response = [
        UserDTO.model_validate(user, from_attributes=True) for user in users
    ]
    return UsersListResultDTO(users=users_response, total=total)


@user_router.get("/{user_id}/")
async def read_user(
    user_id: UserId = Depends(), user_service: UserService = Depends(get_user_service)
) -> UserDTO:
    return await user_service.get_user(user_id)
