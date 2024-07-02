from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.api.dependencies import get_db
from app.core.config import settings
from app.core.db import Base
from app.core.security import create_access_token
from app.main.web import create_app
from app.models import Comment, Post, User
from app.tests.api.models import test_comments, test_posts, test_users

engine_test = create_engine(settings.TEST_DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


TABLES = ["user", "post", "comment"]


def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def prepare_test_db():
    Base.metadata.create_all(bind=engine_test)
    yield


@pytest.fixture(scope="module")
def client(prepare_test_db):
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def clean_tables():
    with SessionLocal() as db:
        with db.begin():
            for table in TABLES:
                db.execute(text(f'TRUNCATE TABLE "{table}" CASCADE;'))


def add_to_db(model: Any):
    with SessionLocal() as db:
        db.add(model)
        db.commit()
        db.refresh(model)
    return model


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


@pytest.fixture
def test_db_user():
    return add_to_db(User(**test_users[0]))


@pytest.fixture
def test_db_users():
    return [add_to_db(User(**user)) for user in test_users]


@pytest.fixture
def test_db_post(test_db_user):
    return add_to_db(Post(**test_posts[0]))


@pytest.fixture
def test_db_posts(test_db_users):
    return [add_to_db(Post(**post)) for post in test_posts]


@pytest.fixture()
def test_db_comment(test_db_post):
    return add_to_db(Comment(**test_comments[0]))


@pytest.fixture()
def test_db_comments(test_db_posts):
    return [add_to_db(Comment(**comment)) for comment in test_comments]


@pytest.fixture
def user_token_1():
    return create_access_token(1)


@pytest.fixture
def user_token_2():
    return create_access_token(2)
