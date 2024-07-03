from fastapi import APIRouter, Depends

from app.api.dependencies import get_comment_service, get_current_auth_user
from app.models.user import User
from app.schemas.comment import (
    CommentDTO,
    CommentsListResultDTO,
    CommentsStatResultDTO,
    CreateCommentDTO,
    CreateCommentRequest,
    DeleteCommentDTO,
    ReadCommentRequest,
    ReadCommentsListDTO,
    ReadCommentsStatDTO,
    ReadCommentsStatRequest,
    UpdateCommentDTO,
    UserCommentData,
)
from app.schemas.pagination import Pagination
from app.schemas.post import PostId
from app.services.comment_service import CommentService

comment_router = APIRouter()


@comment_router.post("/{post_id}/comments/")
async def create_comment(
    body: CreateCommentRequest,
    post_id: PostId = Depends(),
    current_user: User = Depends(get_current_auth_user),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentDTO:
    dto = CreateCommentDTO(
        user_id=current_user.id, post_id=post_id.post_id, **body.model_dump()
    )
    return await comment_service.create_comment(dto)


@comment_router.get("/{post_id}/comments/")
async def read_all_comments(
    post_id: PostId = Depends(),
    pagination: Pagination = Depends(),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentsListResultDTO:
    dto = ReadCommentsListDTO(post_id=post_id.post_id, pagination=pagination)
    return await comment_service.get_post_comments(dto)


@comment_router.get("/{post_id}/comments/{comment_id}/")
async def read_comment(
    query: ReadCommentRequest = Depends(),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentDTO:
    return await comment_service.get_comment(query)


@comment_router.patch("/{post_id}/comments/{comment_id}/")
async def update_comment(
    body: UserCommentData,
    query: ReadCommentRequest = Depends(),
    current_user: User = Depends(get_current_auth_user),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentDTO:
    dto = UpdateCommentDTO(
        user_id=current_user.id, content=body.content, **query.model_dump()
    )
    return await comment_service.update_comment(dto)


@comment_router.delete("/{post_id}/comments/{comment_id}/")
async def delete_comment(
    query: ReadCommentRequest = Depends(),
    current_user: User = Depends(get_current_auth_user),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentDTO:
    dto = DeleteCommentDTO(user_id=current_user.id, **query.model_dump())
    return await comment_service.delete_comment(dto)


@comment_router.get("/{post_id}/comments-daily-breakdown")
async def get_comments_statistics(
    query: ReadCommentsStatRequest = Depends(),
    current_user: User = Depends(get_current_auth_user),
    comment_service: CommentService = Depends(get_comment_service),
) -> list[CommentsStatResultDTO]:
    dto = ReadCommentsStatDTO(user_id=current_user.id, **query.model_dump())
    return await comment_service.get_comment_statisctics(dto)
