from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(settings.DB_URI, future=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
