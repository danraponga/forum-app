from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.models.common.status import Status


class PostDTO(BaseModel):
    id: int
    owner_id: int
    content: str
    status: Status
    created_at: datetime
    updated_at: datetime | None


class PostId(BaseModel):
    post_id: int


class CreatePostRequest(BaseModel):
    content: str
    ai_enabled: bool = False
    ai_delay_minutes: int = 5


class CreatePostDTO(CreatePostRequest):
    user_id: int


class PostsListResultDTO(BaseModel):
    posts: List[PostDTO]
    total: int


class UpdatePostDTO(CreatePostRequest):
    post_id: int
    user_id: int


class DeletePostDTO(BaseModel):
    post_id: int
    user_id: int
