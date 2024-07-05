from datetime import UTC, datetime, timedelta

from app.models.common.enums.status import Status
from app.tests.conftest import test_comments
from app.tests.error_validator import validate_error

API_PREFIX = "/api/posts"


async def test_create_comment(client, test_db_post, mock_comment_data, user_token_1):
    post_id = test_db_post.id
    response = await client.post(
        f"{API_PREFIX}/{post_id}/comments/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == mock_comment_data["content"]
    assert data["post_id"] == post_id
    assert data["owner_id"] == 1


async def test_create_comment_post_not_found(
    client, test_db_user, mock_comment_data, user_token_1
):
    response = await client.post(
        f"{API_PREFIX}/999/comments/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Post not found")


async def test_create_comment_banned(
    client, test_db_post, mock_comment_data, user_token_1
):
    comment_data = mock_comment_data.copy()
    comment_data["content"] = "Fuck"
    response = await client.post(
        f"{API_PREFIX}/{test_db_post.id}/comments/",
        json=comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == Status.BANNED.value


async def test_read_all_comments(client, test_db_comments):
    response = await client.get(f"{API_PREFIX}/1/comments/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["comments"][0]["content"] == test_comments[0]["content"]
    assert data["comments"][1]["content"] == test_comments[1]["content"]


async def test_read_comment(client, test_db_comment):
    response = await client.get(f"{API_PREFIX}/1/comments/1/")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == test_comments[0]["content"]
    assert data["owner_id"] == test_comments[0]["owner_id"]
    assert data["post_id"] == test_comments[0]["post_id"]


async def test_read_comment_not_found(client, test_db_post):
    response = await client.get(f"{API_PREFIX}/1/comments/999/")
    validate_error(response, 404, "Comment not found")


async def test_read_comment_post_not_found(client):
    response = await client.get(f"{API_PREFIX}/999/comments/1/")
    validate_error(response, 404, "Post not found")


async def test_update_comment(client, test_db_comment, mock_comment_data, user_token_1):
    updated_data = mock_comment_data.copy()
    updated_data["content"] = "Updated comment content"
    response = await client.patch(
        f"{API_PREFIX}/1/comments/1/",
        json=updated_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated comment content"


async def test_update_comment_not_found(
    client, test_db_post, mock_comment_data, user_token_1
):
    response = await client.patch(
        f"{API_PREFIX}/1/comments/999/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Comment not found")


async def test_update_comment_profanity(
    client, test_db_comment, mock_comment_data, user_token_1
):
    comment_data = mock_comment_data.copy()
    comment_data["content"] = "Fuck"
    response = await client.patch(
        f"{API_PREFIX}/1/comments/1/",
        json=comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 400, "Content contains profanity")


async def test_update_comment_access_denied(
    client, test_db_comments, mock_comment_data, user_token_2
):
    response = await client.patch(
        f"{API_PREFIX}/1/comments/1/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_2}"},
    )
    validate_error(response, 403, "Access denied")


async def test_update_comment_post_not_found(
    client, test_db_user, mock_comment_data, user_token_1
):
    response = await client.patch(
        f"{API_PREFIX}/999/comments/1/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Post not found")


async def test_delete_comment(client, test_db_comment, user_token_1):
    response = await client.delete(
        f"{API_PREFIX}/1/comments/1/",
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


async def test_delete_comment_not_found(client, test_db_comment, user_token_1):
    response = await client.delete(
        f"{API_PREFIX}/1/comments/999/",
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Comment not found")


async def test_delete_comment_post_not_found(
    client, test_db_user, mock_comment_data, user_token_1
):
    response = await client.delete(
        f"{API_PREFIX}/999/comments/1/",
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Post not found")


async def test_delete_comment_access_denied(client, test_db_comments, user_token_2):
    response = await client.delete(
        f"{API_PREFIX}/1/comments/1/",
        headers={"Authorization": f"Bearer {user_token_2}"},
    )
    validate_error(response, 403, "Access denied")


async def test_get_comments_statistics(client, test_db_comments, user_token_1):
    today = datetime.now(UTC).date()
    tomorrow = today + timedelta(days=1)
    response = await client.get(
        f"{API_PREFIX}/1/comments-daily-breakdown?date_from={today}&date_to={tomorrow}",
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["date"] == today.isoformat()
    assert data[0]["total_comments"] == 4
    assert data[0]["banned_comments"] == 2


async def test_get_comment_statistics_wrong_date(
    client, test_db_comments, user_token_1
):
    response = await client.get(
        f"{API_PREFIX}/1/comments-daily-breakdown?date_from=2024-02-01&date_to=2024-01-01",
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 422
