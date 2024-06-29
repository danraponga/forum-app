from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime


class UsersListResultDTO(BaseModel):
    users: List[UserDTO]
    total: int
