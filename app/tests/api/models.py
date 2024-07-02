from app.models.common.status import Status

test_users = [
    {
        "id": 1,
        "email": "user1@example.com",
        "username": "user1",
        "hashed_password": "password1hash",
    },
    {
        "id": 2,
        "email": "user2@example.com",
        "username": "user2",
        "hashed_password": "password2hash",
    },
]

test_posts = [
    {
        "id": 1,
        "owner_id": 1,
        "content": "Test post1 content",
        "status": Status.ACTIVE,
    },
    {
        "id": 2,
        "owner_id": 2,
        "content": "Test post2 content",
        "status": Status.ACTIVE,
    },
    {
        "id": 3,
        "owner_id": 2,
        "content": "Test post3 content",
        "status": Status.BANNED,
    },
]

test_comments = [
    {
        "id": 1,
        "owner_id": 1,
        "post_id": 1,
        "content": "Test comment1 content",
        "status": Status.ACTIVE,
    },
    {
        "id": 2,
        "owner_id": 1,
        "post_id": 1,
        "content": "Test comment2 content",
        "status": Status.ACTIVE,
    },
    {
        "id": 3,
        "owner_id": 1,
        "post_id": 1,
        "content": "Test comment3 content",
        "status": Status.BANNED,
    },
    {
        "id": 4,
        "owner_id": 1,
        "post_id": 1,
        "content": "Test comment4 content",
        "status": Status.BANNED,
    },
]
