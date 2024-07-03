from datetime import date, datetime
from typing import Any, List

from pydantic import BaseModel, Field, model_validator

from app.models.common.enums.status import Status
from app.schemas.pagination import Pagination
from app.schemas.post import PostId


class CommentDTO(BaseModel):
    id: int
    owner_id: int
    post_id: int
    parent_id: int | None
    content: str
    status: Status
    created_at: datetime
    updated_at: datetime | None


class UserCommentData(BaseModel):
    content: str = Field(examples=["Your content here"])


class CreateCommentRequest(UserCommentData):
    parent_id: int | None = Field(default=None, examples=[None])


class CreateCommentDTO(PostId, CreateCommentRequest):
    user_id: int


class CreateAICommentDTO(BaseModel):
    post_id: int
    parent_id: int


class ReadCommentRequest(PostId):
    comment_id: int


class ReadCommentsListDTO(PostId):
    pagination: Pagination


class CommentsListResultDTO(BaseModel):
    comments: List[CommentDTO]
    total: int


class UpdateCommentDTO(ReadCommentRequest, UserCommentData):
    user_id: int


class DeleteCommentDTO(ReadCommentRequest):
    user_id: int


class ReadCommentsStatRequest(PostId):
    date_from: date
    date_to: date

    @model_validator(mode="before")
    @classmethod
    def validate_dates(cls, data: Any) -> Any:
        if data["date_from"] > data["date_to"]:
            raise ValueError("date_to must be greater than or equal to date_from")
        return data


class ReadCommentsStatDTO(ReadCommentsStatRequest):
    user_id: int


class CommentsStatResultDTO(BaseModel):
    date: date
    total_comments: int
    banned_comments: int
