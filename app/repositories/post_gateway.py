from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.common.enums.status import Status
from app.models.post import Post


class PostDbGateway:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, post: Post) -> None:
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)

    async def get_by_id(self, post_id: int) -> Post | None:
        stmt = select(Post).where(Post.id == post_id, Post.status == Status.ACTIVE)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_posts(self, user_id: int) -> List[Post]:
        stmt = select(Post).where(Post.owner_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_list(self, skip: int, limit: int) -> Tuple[List[Post], int]:
        stmt = (
            select(Post).where(Post.status == Status.ACTIVE).offset(skip).limit(limit)
        )
        result = await self.db.execute(stmt)
        posts = result.scalars().all()
        total = await self.get_total()
        return posts, total

    async def update(self, post: Post, data: dict) -> None:
        allowed_fields = {"content", "ai_enabled", "ai_delay_minutes"}
        for field, value in data.items():
            if field in allowed_fields and value is not None:
                setattr(post, field, value)
        await self.db.commit()
        await self.db.refresh(post)

    async def delete(self, post: Post) -> None:
        await self.db.delete(post)
        await self.db.commit()

    async def get_total(self) -> int:
        stmt = (
            select(func.count()).select_from(Post).where(Post.status == Status.ACTIVE)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()
