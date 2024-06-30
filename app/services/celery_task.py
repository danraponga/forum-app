from celery import Celery

from app.core.config import settings
from app.core.db import SessionLocal
from app.core.utils import generate_ai_response
from app.models import Comment
from app.repositories.comment_gateway import CommentDbGateway
from app.repositories.post_gateway import PostDbGateway
from app.schemas.comment import CreateAICommentDTO

celery = Celery(__name__, broker=settings.REDIS_URL)


@celery.task
def create_comment_by_ai(data: dict):
    post_gateway = PostDbGateway(SessionLocal())
    comment_gateway = CommentDbGateway(SessionLocal())

    dto = CreateAICommentDTO(**data)
    post = post_gateway.get_by_id(dto.post_id)
    if not post:
        return
    parent_comment = comment_gateway.get_by_id(dto.post_id, dto.parent_id)
    if not parent_comment:
        return
    comment = Comment(
        owner_id=post.owner_id,
        post_id=post.id,
        parent_comment_id=parent_comment.id,
        content=generate_ai_response(post.content, parent_comment.content),
    )
    comment_gateway.create(comment)
