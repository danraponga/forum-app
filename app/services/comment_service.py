from app.core.exceptions import EntityNotFoundError, ProfanityContentError
from app.core.utils import contains_profanity
from app.models.comment import Comment
from app.models.common.status import Status
from app.repositories.comment_gateway import CommentDbGateway
from app.repositories.post_gateway import PostDbGateway
from app.schemas.comment import (
    CommentDTO,
    CommentsListResultDTO,
    CreateCommentDTO,
    DeleteCommentDTO,
    ReadCommentsListDTO,
    UpdateCommentDTO,
)
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
