from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import (
    get_comment_gateway,
    get_comment_service,
    get_current_auth_user,
    get_post_gateway,
)
from app.core.exceptions import EntityNotFoundError, ProfanityContentError
from app.models.user import User
from app.repositories.comment_gateway import CommentDbGateway
from app.repositories.post_gateway import PostDbGateway
from app.schemas.comment import (
    CommentDTO,
    CommentsListResultDTO,
    CreateCommentDTO,
    CreateCommentRequest,
    DeleteCommentDTO,
    ReadCommentRequest,
    ReadCommentsListDTO,
    UpdateCommentDTO,
    UserCommentData,
)
from app.schemas.pagination import Pagination
from app.schemas.post import PostId
from app.services.comment_service import CommentService

comment_router = APIRouter()


@comment_router.post("/create")
def create_comment(
    body: CreateCommentRequest,
    post_id: PostId = Depends(),
    current_user: User = Depends(get_current_auth_user),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentDTO:
    dto = CreateCommentDTO(
        user_id=current_user.id, post_id=post_id.post_id, **body.model_dump()
    )
    try:
        return comment_service.create_comment(dto)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=e)


@comment_router.get("/")
def read_all_comments(
    post_id: PostId = Depends(),
    pagination: Pagination = Depends(),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentsListResultDTO:
    dto = ReadCommentsListDTO(post_id=post_id.post_id, pagination=pagination)
    try:
        return comment_service.get_post_comments(dto)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")


@comment_router.get("/{comment_id}")
def read_comment(
    query: ReadCommentRequest = Depends(),
    post_gateway: PostDbGateway = Depends(get_post_gateway),
    comment_gateway: CommentDbGateway = Depends(get_comment_gateway),
) -> CommentDTO:
    if not post_gateway.get_by_id(query.post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    comment = comment_gateway.get_by_id(query.post_id, query.comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return CommentDTO.model_validate(comment, from_attributes=True)


@comment_router.patch("/{comment_id}")
def update_comment(
    body: UserCommentData,
    query: ReadCommentRequest = Depends(),
    current_user: User = Depends(get_current_auth_user),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentDTO:
    dto = UpdateCommentDTO(
        user_id=current_user.id, content=body.content, **query.model_dump()
    )
    try:
        return comment_service.update_comment(dto)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=e)
    except ProfanityContentError:
        raise HTTPException(status_code=400, detail="Profanity content")


@comment_router.delete("/{comment_id}")
def delete_comment(
    query: ReadCommentRequest = Depends(),
    current_user: User = Depends(get_current_auth_user),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentDTO:
    dto = DeleteCommentDTO(user_id=current_user.id, **query.model_dump())
    try:
        return comment_service.delete_comment(dto)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=e)
