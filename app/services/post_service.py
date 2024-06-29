from app.core.exceptions import EntityNotFoundError, ProfanityContentError
from app.core.utils import contains_profanity
from app.models import Post
from app.models.common.status import Status
from app.repositories.post_gateway import PostDbGateway
from app.schemas.post import (
    CreatePostDTO,
    DeletePostDTO,
    PostDTO,
    UpdatePostDTO,
)
from app.services.common.base_service import BaseService


class PostService(BaseService):
    def __init__(self, post_gateway: PostDbGateway) -> None:
        self.post_gateway = post_gateway

    def create_post(self, dto: CreatePostDTO) -> PostDTO:
        post = Post(
            owner_id=dto.user_id,
            content=dto.content,
            ai_enabled=dto.ai_enabled,
            ai_delay_minutes=dto.ai_delay_minutes,
        )
        if contains_profanity(dto.content):
            post.status = Status.BANNED

        self.post_gateway.create(post)
        return PostDTO.model_validate(post, from_attributes=True)

    def update_post(self, dto: UpdatePostDTO) -> PostDTO:
        post = self.post_gateway.get_by_id(dto.post_id)
        if not post:
            raise EntityNotFoundError()
        self.ensure_can_edit(post.owner_id, dto.user_id)

        if contains_profanity(dto.content):
            raise ProfanityContentError()

        self.post_gateway.update(post, dto.model_dump())
        return PostDTO.model_validate(post, from_attributes=True)

    def delete_post(self, dto: DeletePostDTO) -> PostDTO:
        post = self.post_gateway.get_by_id(dto.post_id)
        if not post:
            raise EntityNotFoundError()
        self.ensure_can_edit(post.owner_id, dto.user_id)

        self.post_gateway.delete(post)
        return PostDTO.model_validate(post, from_attributes=True)
