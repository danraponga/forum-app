from datetime import datetime
from typing import List, Tuple

from sqlalchemy import Row, case, func, select
from sqlalchemy import update as sqla_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from app.models.comment import Comment
from app.models.common.status import Status


class CommentDbGateway:
    def __init__(self, session: AsyncSession) -> None:
        self.db = session

    async def create(self, comment: Comment) -> None:
        self.db.add(comment)
        await self.db.commit()

    async def get_by_id(self, post_id: int, comment_id: int) -> Comment:
        result = await self.db.execute(
            select(Comment).filter(
                Comment.post_id == post_id,
                Comment.id == comment_id,
                Comment.status == Status.ACTIVE,
            )
        )
        return result.scalars().first()

    async def get_list_by_post_id(
        self, post_id: int, skip: int, limit: int
    ) -> Tuple[List[Comment], int]:
        query = (
            select(Comment)
            .filter(Comment.post_id == post_id, Comment.status == Status.ACTIVE)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        comments = result.scalars().all()
        total = await self.get_total(query)
        return comments, total

    async def get_list_by_parent_id(
        self, parent_id: int, skip: int, limit: int
    ) -> Tuple[List[Comment], int]:
        query = (
            select(Comment)
            .filter(
                Comment.parent_comment_id == parent_id, Comment.status == Status.ACTIVE
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        comments = result.scalars().all()
        total = await self.get_total(query)
        return comments, total

    async def update(self, comment: Comment, data: dict) -> None:
        allowed_fields = ["content"]
        for field, value in data.items():
            if field in allowed_fields and value:
                setattr(comment, field, value)
        self.db.commit()

    async def delete(self, comment: Comment) -> None:
        await self.db.delete(comment)
        await self.db.commit()

    async def get_total(self, query: Query) -> int:
        result = await self.db.execute(query)
        return len(result.scalars().all())

    async def get_statistics_by_date(
        self, date_from: datetime, date_to: datetime, post_id: int
    ) -> List[Row]:
        result = await self.db.execute(
            select(
                func.date(Comment.created_at).label("date"),
                func.count(Comment.id).label("total_comments"),
                func.sum(case((Comment.status == Status.BANNED, 1), else_=0)).label(
                    "banned_comments"
                ),
            )
            .filter(
                Comment.post_id == post_id,
                Comment.created_at >= date_from,
                Comment.created_at <= date_to,
            )
            .group_by(func.date(Comment.created_at))
        )
        return result.fetchall()
