from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import (
    get_current_auth_user,
    get_post_gateway,
    get_post_service,
)
from app.api.routers.comment import comment_router
from app.models.user import User
from app.repositories.post_gateway import PostDbGateway
from app.schemas.pagination import Pagination
from app.schemas.post import (
    CreatePostDTO,
    CreatePostRequest,
    DeletePostDTO,
    PostDTO,
    PostId,
    PostsListResultDTO,
    UpdatePostDTO,
)
from app.services.post_service import PostService

post_router = APIRouter()
post_router.include_router(comment_router, tags=["Comments"])


@post_router.post("/create/")
def create_post(
    user_data: CreatePostRequest,
    current_user: User = Depends(get_current_auth_user),
    post_service: PostService = Depends(get_post_service),
) -> PostDTO:
    dto = CreatePostDTO(user_id=current_user.id, **user_data.model_dump())
    return post_service.create_post(dto)


@post_router.get("/")
def read_posts_all(
    pagination: Pagination = Depends(),
    post_gateway: PostDbGateway = Depends(get_post_gateway),
) -> PostsListResultDTO:
    posts, total = post_gateway.get_list(pagination.skip, pagination.limit)

    posts_response = [
        PostDTO.model_validate(post, from_attributes=True) for post in posts
    ]
    return PostsListResultDTO(posts=posts_response, total=total)


@post_router.get("/{post_id}/")
def read_post(
    post_id: PostId = Depends(),
    post_service: PostService = Depends(get_post_service),
) -> PostDTO:
    return post_service.get_post(post_id)


@post_router.patch("/{post_id}/")
def update_post(
    user_data: CreatePostRequest,
    post_id: PostId = Depends(),
    current_user: User = Depends(get_current_auth_user),
    post_service: PostService = Depends(get_post_service),
) -> PostDTO:
    dto = UpdatePostDTO(
        post_id=post_id.post_id, user_id=current_user.id, **user_data.model_dump()
    )
    return post_service.update_post(dto)


@post_router.delete("/{post_id}/")
def delete_post(
    post_id: PostId = Depends(),
    current_user: User = Depends(get_current_auth_user),
    post_service: PostService = Depends(get_post_service),
) -> PostDTO:
    dto = DeletePostDTO(post_id=post_id.post_id, user_id=current_user.id)
    return post_service.delete_post(dto)
