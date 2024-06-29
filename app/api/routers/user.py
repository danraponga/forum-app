from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_user_gateway
from app.repositories.user_gateway import UserDbGateway
from app.schemas.pagination import Pagination
from app.schemas.user import UserDTO, UsersListResultDTO

user_router = APIRouter()


@user_router.get("/")
def read_users_all(
    pagination: Pagination = Depends(),
    user_gateway: UserDbGateway = Depends(get_user_gateway),
) -> UsersListResultDTO:
    users = user_gateway.get_list(pagination.skip, pagination.limit)
    total = user_gateway.get_total()

    users_response = [
        UserDTO.model_validate(user, from_attributes=True) for user in users
    ]
    return UsersListResultDTO(users=users_response, total=total)


@user_router.get("/{user_id}")
def read_user(
    user_id: int, user_gateway: UserDbGateway = Depends(get_user_gateway)
) -> UserDTO:
    user = user_gateway.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDTO.model_validate(user, from_attributes=True)
