from datetime import datetime
from app.core.utils import generate_ai_response
from app.models.comment import Comment
from app.core.db import sessionmanager
from app.repositories.comment_gateway import CommentDbGateway
from app.repositories.post_gateway import PostDbGateway


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore

from app.schemas.comment import CreateAICommentDTO

from app.core.config import settings


jobstores = {"default": RedisJobStore(host=settings.REDIS_HOST, port=settings.REDIS_PORT)}
scheduler = AsyncIOScheduler(jobstores=jobstores)


def schedule_create_comment_by_ai_task(dto: CreateAICommentDTO, run_date: datetime) -> None:
    scheduler.add_job(
        create_comment_by_ai, trigger="date", run_date=run_date, args=[dto]
    )


async def create_comment_by_ai(dto: CreateAICommentDTO) -> None:
    async with sessionmanager.session() as db:
        post_gateway = PostDbGateway(db)
        comment_gateway = CommentDbGateway(db)
    post = await post_gateway.get_by_id(dto.post_id)
    if not post:
        return
    parent = await comment_gateway.get_by_id(dto.post_id, dto.parent_id)
    if not parent:
        return

    ai_response = generate_ai_response(post.content, parent.content)

    comment = Comment(
        owner_id=post.owner_id,
        post_id=post.id,
        parent_id=parent.id,
        content=ai_response,
    )
    await comment_gateway.create(comment)
    await db.close()
    print("task successfully completed")
