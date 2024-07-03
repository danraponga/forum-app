from app.core.exceptions.common import ProfanityContent
from app.core.exceptions.entity import PostNotFound
from app.core.utils import contains_profanity
from app.models import Post
from app.models.common.enums.status import Status
from app.repositories.post_gateway import PostDbGateway
from app.schemas.post import (
    CreatePostDTO,
    DeletePostDTO,
    PostDTO,
    PostId,
    UpdatePostDTO,
)
from app.services.common.base_service import BaseService


class PostService(BaseService):
    def __init__(self, post_gateway: PostDbGateway) -> None:
        self.post_gateway = post_gateway

    async def create_post(self, dto: CreatePostDTO) -> PostDTO:
        post = Post(
            owner_id=dto.user_id,
            content=dto.content,
            ai_enabled=dto.ai_enabled,
            ai_delay_minutes=dto.ai_delay_minutes,
        )
        if contains_profanity(dto.content):
            post.status = Status.BANNED

        await self.post_gateway.create(post)
        return PostDTO.model_validate(post, from_attributes=True)

    async def get_post(self, dto: PostId) -> PostDTO:
        post = await self.post_gateway.get_by_id(dto.post_id)
        if not post:
            raise PostNotFound()
        return PostDTO.model_validate(post, from_attributes=True)

    async def update_post(self, dto: UpdatePostDTO) -> PostDTO:
        post = await self.post_gateway.get_by_id(dto.post_id)
        if not post:
            raise PostNotFound()
        self.ensure_can_edit(post.owner_id, dto.user_id)

        if contains_profanity(dto.content):
            raise ProfanityContent()

        await self.post_gateway.update(post, dto.model_dump())
        return PostDTO.model_validate(post, from_attributes=True)

    async def delete_post(self, dto: DeletePostDTO) -> PostDTO:
        post = await self.post_gateway.get_by_id(dto.post_id)
        if not post:
            raise PostNotFound()
        self.ensure_can_edit(post.owner_id, dto.user_id)

        await self.post_gateway.delete(post)
        return PostDTO.model_validate(post, from_attributes=True)
