from datetime import datetime
from typing import List, Tuple

from sqlalchemy import Row, case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.models.common.enums.status import Status


class CommentDbGateway:
    def __init__(self, session: AsyncSession) -> None:
        self.db = session

    async def create(self, comment: Comment) -> None:
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)

    async def get_by_id(self, post_id: int, comment_id: int) -> Comment | None:
        stmt = select(Comment).where(
            Comment.post_id == post_id,
            Comment.id == comment_id,
            Comment.status == Status.ACTIVE,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_list_by_post_id(
        self, post_id: int, skip: int, limit: int
    ) -> Tuple[List[Comment], int]:
        stmt = (
            select(Comment)
            .where(Comment.post_id == post_id, Comment.status == Status.ACTIVE)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        comments = result.scalars().all()
        total = await self.get_total(stmt)
        return comments, total

    async def update(self, comment: Comment, data: dict) -> None:
        allowed_fields = ["content"]
        for field, value in data.items():
            if field in allowed_fields and value is not None:
                setattr(comment, field, value)
        await self.db.commit()
        await self.db.refresh(comment)

    async def delete(self, comment: Comment) -> None:
        await self.db.delete(comment)
        await self.db.commit()

    async def get_total(self, stmt) -> int:
        count_stmt = stmt.with_only_columns(func.count()).order_by(None)
        result = await self.db.execute(count_stmt)
        return result.scalar_one()

    async def get_statistics_by_date(
        self, date_from: datetime, date_to: datetime, post_id: int
    ) -> List[Row]:
        stmt = (
            select(
                func.date(Comment.created_at).label("date"),
                func.count(Comment.id).label("total_comments"),
                func.sum(case((Comment.status == Status.BANNED, 1), else_=0)).label(
                    "banned_comments"
                ),
            )
            .where(
                Comment.post_id == post_id,
                Comment.created_at >= date_from,
                Comment.created_at <= date_to,
            )
            .group_by(func.date(Comment.created_at))
        )
        result = await self.db.execute(stmt)
        return result.all()
