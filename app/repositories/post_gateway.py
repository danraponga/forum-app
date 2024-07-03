from typing import List

from sqlalchemy import func
from sqlalchemy import update as sqla_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.common.status import Status
from app.models.post import Post


class PostDbGateway:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, post: Post) -> None:
        self.db.add(post)
        await self.db.commit()

    async def get_by_id(self, post_id: int) -> Post:
        result = await self.db.execute(
            select(Post).filter(Post.id == post_id, Post.status == Status.ACTIVE)
        )
        return result.scalars().first()

    async def get_user_posts(self, user_id: int) -> List[Post]:
        result = await self.db.execute(select(Post).filter(Post.owner_id == user_id))
        return result.scalars().all()

    async def get_list(self, skip: int, limit: int) -> List[Post]:
        result = await self.db.execute(
            select(Post).filter(Post.status == Status.ACTIVE).offset(skip).limit(limit)
        )
        posts = result.scalars().all()
        total = await self.get_total()
        return posts, total

    async def update(self, post: Post, data: dict) -> None:
        allowed_fields = {
            "content",
            "ai_enabled",
            "ai_delay_minutes",
        }
        for field, value in data.items():
            if field in allowed_fields and value:
                setattr(post, field, value)
        self.db.commit()

    async def delete(self, post: Post) -> None:
        await self.db.delete(post)
        await self.db.commit()

    async def get_total(self) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Post).filter(Post.status == Status.ACTIVE)
        )
        return result.scalar_one()
