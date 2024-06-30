from typing import List

from app.core.exceptions import EntityNotFoundError, ProfanityContentError
from app.core.utils import contains_profanity
from app.models.comment import Comment
from app.models.common.status import Status
from app.repositories.comment_gateway import CommentDbGateway
from app.repositories.post_gateway import PostDbGateway
from app.schemas.comment import (
    CommentDTO,
    CommentsListResultDTO,
    CommentsStatResultDTO,
    CreateAICommentDTO,
    CreateCommentDTO,
    DeleteCommentDTO,
    ReadCommentsListDTO,
    ReadCommentsStatDTO,
    UpdateCommentDTO,
)
from app.services.celery_task import create_comment_by_ai
from app.services.common.base_service import BaseService


class CommentService(BaseService):
    def __init__(
        self, comment_gateway: CommentDbGateway, post_gateway: PostDbGateway
    ) -> None:
        self.comment_gateway = comment_gateway
        self.post_gateway = post_gateway

    def create_comment(self, dto: CreateCommentDTO) -> CommentDTO:
        post = self.post_gateway.get_by_id(dto.post_id)
        if not post:
            raise EntityNotFoundError("Post not found")
        if dto.parent_comment_id:
            if not self.comment_gateway.get_by_id(dto.post.id, dto.parent_comment_id):
                raise EntityNotFoundError("Comment not found")

        comment = Comment(
            owner_id=dto.user_id,
            post_id=dto.post_id,
            parent_comment_id=dto.parent_comment_id,
            content=dto.content,
        )
        if contains_profanity(dto.content):
            comment.status = Status.BANNED
        self.comment_gateway.create(comment)

        if post.ai_enabled and post.owner_id != comment.owner_id:
            dto = CreateAICommentDTO(
                post_id=post.id,
                parent_id=comment.id,
            )
            create_comment_by_ai.apply_async(
                [dto.model_dump()], countdown=post.ai_delay_minutes * 60
            )
        return CommentDTO.model_validate(comment, from_attributes=True)

    def get_post_comments(self, dto: ReadCommentsListDTO) -> CommentsListResultDTO:
        if not self.post_gateway.get_by_id(dto.post_id):
            raise EntityNotFoundError()

        comments, total = self.comment_gateway.get_list_by_post_id(
            dto.post_id, dto.pagination.skip, dto.pagination.limit
        )
        comments_dto_list = [
            CommentDTO.model_validate(comment, from_attributes=True)
            for comment in comments
        ]
        return CommentsListResultDTO(comments=comments_dto_list, total=total)

    def update_comment(self, dto: UpdateCommentDTO) -> CommentDTO:
        if not self.post_gateway.get_by_id(dto.post_id):
            raise EntityNotFoundError("Post not found")

        comment = self.comment_gateway.get_by_id(dto.post_id, dto.comment_id)
        if not comment:
            raise EntityNotFoundError("Comment not found")
        self.ensure_can_edit(comment.owner_id, dto.user_id)

        if contains_profanity(dto.content):
            raise ProfanityContentError()

        self.comment_gateway.update(comment, dto.model_dump())
        return CommentDTO.model_validate(comment, from_attributes=True)

    def delete_comment(self, dto: DeleteCommentDTO) -> CommentDTO:
        if not self.post_gateway.get_by_id(dto.post_id):
            raise EntityNotFoundError("Post not found")

        comment = self.comment_gateway.get_by_id(dto.post_id, dto.comment_id)
        if not comment:
            raise EntityNotFoundError("Comment not found")
        self.ensure_can_edit(comment.owner_id, dto.user_id)

        self.comment_gateway.delete(comment)
        return CommentDTO.model_validate(comment, from_attributes=True)

    def get_comment_statisctics(
        self, dto: ReadCommentsStatDTO
    ) -> List[CommentsStatResultDTO]:
        post = self.post_gateway.get_by_id(dto.post_id)
        if not post:
            raise EntityNotFoundError()
        self.ensure_can_edit(post.owner_id, dto.user_id)

        statistics = self.comment_gateway.get_statistics_by_date(
            date_from=dto.date_from, date_to=dto.date_to, post_id=dto.post_id
        )
        return [
            CommentsStatResultDTO.model_validate(row, from_attributes=True)
            for row in statistics
        ]
