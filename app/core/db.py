from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.core.config import settings


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


async_engine = create_async_engine(settings.DB_URI, future=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
