from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, model_validator

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
    ai_enabled: bool = Field(examples=[False])
    ai_delay_minutes: int = Field(examples=[5])
    
    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: dict) -> dict:
        if data["ai_delay_minutes"] < 0:
            raise ValueError("Delay can't be less than zero. Minimum allowed value: 0")
        return data
        

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
