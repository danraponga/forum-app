import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.dependencies import get_db
from app.core.config import settings
from app.core.db import Base
from app.core.security import create_access_token
from app.main.web import create_app
from app.models import Comment, Post, User
from app.tests.api.models import test_comments, test_posts, test_users

async_engine = create_async_engine(settings.TEST_DB_URI, echo=True)
async_session = async_sessionmaker(
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    bind=async_engine,
)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def override_get_db():
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_engine,
    )
    async with async_session() as db:
        yield db


# @pytest.fixture(scope="function", autouse=True)
# async def async_db():
#     async_session = async_sessionmaker(
#         expire_on_commit=False,
#         autocommit=False,
#         autoflush=False,
#         bind=async_engine,
#     )
#     async with async_session() as db:
#         yield db


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    app = create_app()
    transport = ASGITransport(app=app)
    app.dependency_overrides[get_db] = override_get_db
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.fixture
def mock_user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password",
    }


@pytest.fixture
def mock_login_data(mock_user_data):
    return {
        "email": mock_user_data["email"],
        "password": mock_user_data["password"],
    }


@pytest.fixture
def mock_post_data():
    return {
        "content": "Test post content",
        "ai_enabled": False,
        "ai_delay_minutes": 0,
    }


@pytest.fixture
def mock_comment_data():
    return {"content": "Test comment content"}


async def add_model(model):
    async with async_session() as db:
        db.add(model)
        await db.commit()
        await db.refresh(model)
    return model


@pytest.fixture
async def test_db_user():
    # user = User(**test_users[0])
    # async_db.add(user)
    # await async_db.commit()
    # await async_db.refresh(user)
    # return user
    return await add_model(User(**test_users[0]))


@pytest.fixture
async def test_db_users():
    return [await add_model(User(**user)) for user in test_users]


@pytest.fixture
async def test_db_post(test_db_user):
    return await add_model(Post(**test_posts[0]))


@pytest.fixture
async def test_db_posts(test_db_users):
    return [await add_model(Post(**post)) for post in test_posts]


@pytest.fixture()
async def test_db_comment(test_db_post):
    return await add_model(Comment(**test_comments[0]))


@pytest.fixture()
async def test_db_comments(test_db_posts):
    return [await add_model(Comment(**comment)) for comment in test_comments]


@pytest.fixture
async def user_token_1():
    return create_access_token(1)


@pytest.fixture
async def user_token_2():
    return create_access_token(2)
