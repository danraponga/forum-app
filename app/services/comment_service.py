from datetime import datetime, timedelta
from typing import List

from app.core.exceptions.common import ProfanityContent
from app.core.exceptions.entity import CommentNotFound, PostNotFound
from app.core.utils import contains_profanity
from app.models.comment import Comment
from app.models.common.enums.status import Status
from app.repositories.comment_gateway import CommentDbGateway
from app.repositories.post_gateway import PostDbGateway
from app.schemas.comment import (
    CommentDTO,
    CommentsListResultDTO,
    CommentsStatResultDTO,
    CreateAICommentDTO,
    CreateCommentDTO,
    DeleteCommentDTO,
    ReadCommentRequest,
    ReadCommentsListDTO,
    ReadCommentsStatDTO,
    UpdateCommentDTO,
)
from app.services.scheduler import schedule_create_comment_by_ai_task
from app.services.common.base_service import BaseService


class CommentService(BaseService):
    def __init__(
        self, comment_gateway: CommentDbGateway, post_gateway: PostDbGateway
    ) -> None:
        self.comment_gateway = comment_gateway
        self.post_gateway = post_gateway

    async def create_comment(self, dto: CreateCommentDTO) -> CommentDTO:
        post = await self.post_gateway.get_by_id(dto.post_id)
        if not post:
            raise PostNotFound()
        if dto.parent_id:
            if not await self.comment_gateway.get_by_id(dto.post_id, dto.parent_id):
                raise CommentNotFound()

        comment = Comment(
            owner_id=dto.user_id,
            post_id=dto.post_id,
            parent_id=dto.parent_id,
            content=dto.content,
        )
        if contains_profanity(dto.content):
            comment.status = Status.BANNED
        await self.comment_gateway.create(comment)

        if post.ai_enabled and post.owner_id != comment.owner_id:
            ai_dto = CreateAICommentDTO(
                post_id=post.id,
                parent_id=comment.id,
            )
            run_date = datetime.now() + timedelta(minutes=post.ai_delay_minutes)
            schedule_create_comment_by_ai_task(ai_dto, run_date)
            
        return CommentDTO.model_validate(comment, from_attributes=True)

    async def get_comment(self, dto: ReadCommentRequest) -> CommentDTO:
        if not await self.post_gateway.get_by_id(dto.post_id):
            raise PostNotFound()
        comment = await self.comment_gateway.get_by_id(dto.post_id, dto.comment_id)
        if not comment:
            raise CommentNotFound()
        return CommentDTO.model_validate(comment, from_attributes=True)

    async def get_post_comments(
        self, dto: ReadCommentsListDTO
    ) -> CommentsListResultDTO:
        if not await self.post_gateway.get_by_id(dto.post_id):
            raise PostNotFound()

        comments, total = await self.comment_gateway.get_list_by_post_id(
            dto.post_id, dto.pagination.skip, dto.pagination.limit
        )
        comments_dto_list = [
            CommentDTO.model_validate(comment, from_attributes=True)
            for comment in comments
        ]
        return CommentsListResultDTO(comments=comments_dto_list, total=total)

    async def update_comment(self, dto: UpdateCommentDTO) -> CommentDTO:
        if not await self.post_gateway.get_by_id(dto.post_id):
            raise PostNotFound()

        comment = await self.comment_gateway.get_by_id(dto.post_id, dto.comment_id)
        if not comment:
            raise CommentNotFound()
        self.ensure_can_edit(comment.owner_id, dto.user_id)

        if contains_profanity(dto.content):
            raise ProfanityContent()

        await self.comment_gateway.update(comment, dto.model_dump())
        return CommentDTO.model_validate(comment, from_attributes=True)

    async def delete_comment(self, dto: DeleteCommentDTO) -> CommentDTO:
        if not await self.post_gateway.get_by_id(dto.post_id):
            raise PostNotFound()

        comment = await self.comment_gateway.get_by_id(dto.post_id, dto.comment_id)
        if not comment:
            raise CommentNotFound()
        self.ensure_can_edit(comment.owner_id, dto.user_id)

        await self.comment_gateway.delete(comment)
        return CommentDTO.model_validate(comment, from_attributes=True)

    async def get_comment_statisctics(
        self, dto: ReadCommentsStatDTO
    ) -> List[CommentsStatResultDTO]:
        post = await self.post_gateway.get_by_id(dto.post_id)
        if not post:
            raise PostNotFound()
        self.ensure_can_edit(post.owner_id, dto.user_id)

        statistics = await self.comment_gateway.get_statistics_by_date(
            date_from=dto.date_from, date_to=dto.date_to, post_id=dto.post_id
        )
        return [
            CommentsStatResultDTO.model_validate(row, from_attributes=True)
            for row in statistics
        ]
