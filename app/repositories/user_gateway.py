from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User


class UserDbGateway:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user: User) -> None:
        self.db.add(user)
        await self.db.commit()

    async def get_by_id(self, user_id: int) -> User:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> User:
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().one_or_none()

    async def get_by_username(self, username: str) -> User:
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def get_list(self, skip: int, limit: int) -> tuple[list[User], int]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        users = result.scalars().all()
        total = await self.get_total()
        return users, total

    async def get_total(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(User))
        return result.scalar_one()
