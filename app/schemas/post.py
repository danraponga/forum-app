from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models.common.enums.status import Status


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
    content: str = Field(examples=["Your content here"])
    ai_enabled: bool = False
    ai_delay_minutes: int | None = None


class CreatePostDTO(CreatePostRequest):
    user_id: int


class PostsListResultDTO(BaseModel):
    posts: List[PostDTO]
    total: int


class UpdatePostBase(BaseModel):
    post_id: int
    user_id: int


class UpdatePostDTO(UpdatePostBase, CreatePostRequest):
    pass


class DeletePostDTO(UpdatePostBase):
    pass
