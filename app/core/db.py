import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncConnection, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(url=db_url, future=True, echo=False)
        self._sessionmaker = async_sessionmaker(
            bind=self._engine, autocommit=False, expire_on_commit=False
        )

    async def close(self):
        await self._engine.dispose()
        self._sessionmaker = None
        self._engine = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.begin() as connection:
                try:
                    yield connection
                except Exception:
                    await connection.rollback()
                    raise
                
    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
                        

sessionmanager = DatabaseSessionManager(settings.DB_URI)
