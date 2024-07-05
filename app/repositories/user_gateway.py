from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserDbGateway:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user: User) -> None:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_list(self, skip: int, limit: int) -> tuple[list[User], int]:
        stmt = select(User).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        total = await self.get_total()
        return users, total

    async def get_total(self) -> int:
        stmt = select(func.count()).select_from(User)
        result = await self.db.execute(stmt)
        return result.scalar_one()
