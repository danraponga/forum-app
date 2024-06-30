from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models.common.status import Status
from app.schemas.pagination import Pagination
from app.schemas.post import PostId


class CommentDTO(BaseModel):
    id: int
    owner_id: int
    post_id: int
    parent_comment_id: int | None
    content: str
    status: Status
    created_at: datetime
    updated_at: datetime | None


class UserCommentData(BaseModel):
    content: str = Field(examples=["Your content here"])


class CreateCommentRequest(UserCommentData):
    parent_comment_id: int | None = Field(default=None, examples=[None])


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
