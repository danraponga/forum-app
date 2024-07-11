from datetime import datetime

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.schemas.comment import CreateAICommentDTO
from app.services.ai_comment_response_task import create_comment_response_by_ai

jobstores = {
    "default": RedisJobStore(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
}
scheduler = AsyncIOScheduler(jobstores=jobstores)


async def schedule_ai_comment_response_task(
    dto: CreateAICommentDTO, run_date: datetime
) -> None:
    scheduler.add_job(
        create_comment_response_by_ai, trigger="date", run_date=run_date, args=[dto]
    )
    print(f'Task "create_comment_response_by_ai" will be started at {run_date}')
