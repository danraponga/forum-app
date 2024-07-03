from app.core.security import create_access_token
from app.models.common.status import Status
from app.tests.conftest import test_posts, test_users
from app.tests.error_validator import validate_error

API_PREFIX = "/api/posts"


async def test_create_post(client, test_db_user, mock_post_data):
    token = create_access_token(1)
    response = await client.post(
        f"{API_PREFIX}/create/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == mock_post_data["content"]
    assert data["owner_id"] == test_db_user.id


async def test_create_post_banned(client, test_db_user, mock_post_data):
    post_data = mock_post_data.copy()
    post_data["content"] = "Fuck"
    token = create_access_token(1)

    response = await client.post(
        f"{API_PREFIX}/create/",
        json=post_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == Status.BANNED.value


async def test_read_posts_all(client, test_db_posts):
    response = await client.get(f"{API_PREFIX}/")
    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 2
    assert data["posts"][0]["content"] == test_posts[0]["content"]
    assert data["posts"][1]["content"] == test_posts[1]["content"]


async def test_read_post(client, test_db_post):
    response = await client.get(f"{API_PREFIX}/{test_db_post.id}/")
    assert response.status_code == 200

    data = response.json()
    assert data["owner_id"] == test_users[0]["id"]
    assert data["content"] == test_posts[0]["content"]


async def test_read_post_not_found(client):
    response = await client.get(f"{API_PREFIX}/999/")
    validate_error(response, 404, "Post not found")


async def test_update_post(client, test_db_post, mock_post_data):
    updated_data = mock_post_data.copy()
    updated_data["content"] = "Updated content"
    token = create_access_token(1)

    response = await client.patch(
        f"{API_PREFIX}/1/",
        json=updated_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["content"] == "Updated content"


async def test_update_post_not_found(client, test_db_user, mock_post_data):
    token = create_access_token(1)

    response = await client.patch(
        f"{API_PREFIX}/999/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    validate_error(response, 404, "Post not found")


async def test_update_post_access_denied(client, test_db_posts, mock_post_data):
    token = create_access_token(2)

    response = await client.patch(
        f"{API_PREFIX}/1/",
        json=mock_post_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    validate_error(response, 403, "Access denied")


async def test_update_post_profanity_error(client, test_db_post, mock_post_data):
    updated_data = mock_post_data.copy()
    updated_data["content"] = "Fuck"
    token = create_access_token(1)

    response = await client.patch(
        f"{API_PREFIX}/1/",
        json=updated_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    validate_error(response, 400, "Content contains profanity")


async def test_delete_post(client, test_db_posts):
    token = create_access_token(1)
    response = await client.delete(
        f"{API_PREFIX}/1/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1


async def test_delete_post_not_found(client, test_db_user):
    token = create_access_token(1)
    response = await client.delete(
        f"{API_PREFIX}/999/", headers={"Authorization": f"Bearer {token}"}
    )
    validate_error(response, 404, "Post not found")


async def test_delete_post_access_denied(client, test_db_posts):
    token = create_access_token(2)
    response = await client.delete(
        f"{API_PREFIX}/1/", headers={"Authorization": f"Bearer {token}"}
    )
    validate_error(response, 403, "Access denied")
