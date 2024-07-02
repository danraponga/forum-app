from datetime import date, timedelta

from app.models.common.status import Status
from app.tests.conftest import test_comments
from app.tests.error_validator import validate_error

API_PREFIX = "/api/posts"


def test_create_comment(client, test_db_post, mock_comment_data, user_token_1):
    post_id = test_db_post.id
    response = client.post(
        f"{API_PREFIX}/{post_id}/comments/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == mock_comment_data["content"]
    assert data["post_id"] == post_id
    assert data["owner_id"] == 1


def test_create_comment_post_not_found(
    client, test_db_user, mock_comment_data, user_token_1
):
    response = client.post(
        f"{API_PREFIX}/999/comments/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Post not found")


def test_create_comment_banned(client, test_db_post, mock_comment_data, user_token_1):
    comment_data = mock_comment_data.copy()
    comment_data["content"] = "Fuck"
    response = client.post(
        f"{API_PREFIX}/{test_db_post.id}/comments/",
        json=comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == Status.BANNED.value


def test_read_all_comments(client, test_db_comments):
    response = client.get(f"{API_PREFIX}/1/comments/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["comments"][0]["content"] == test_comments[0]["content"]
    assert data["comments"][1]["content"] == test_comments[1]["content"]


def test_read_comment(client, test_db_comment):
    response = client.get(f"{API_PREFIX}/1/comments/1/")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == test_comments[0]["content"]
    assert data["owner_id"] == test_comments[0]["owner_id"]
    assert data["post_id"] == test_comments[0]["post_id"]


def test_read_comment_not_found(client, test_db_post):
    response = client.get(f"{API_PREFIX}/1/comments/999/")
    validate_error(response, 404, "Comment not found")


def test_read_comment_post_not_found(client):
    response = client.get(f"{API_PREFIX}/999/comments/1/")
    validate_error(response, 404, "Post not found")


def test_update_comment(client, test_db_comment, mock_comment_data, user_token_1):
    updated_data = mock_comment_data.copy()
    updated_data["content"] = "Updated comment content"
    response = client.patch(
        f"{API_PREFIX}/1/comments/1/",
        json=updated_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated comment content"


def test_update_comment_not_found(
    client, test_db_post, mock_comment_data, user_token_1
):
    response = client.patch(
        f"{API_PREFIX}/1/comments/999/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Comment not found")


def test_update_comment_profanity(
    client, test_db_comment, mock_comment_data, user_token_1
):
    comment_data = mock_comment_data.copy()
    comment_data["content"] = "Fuck"
    response = client.patch(
        f"{API_PREFIX}/1/comments/1/",
        json=comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 400, "Content contains profanity")


def test_update_comment_access_denied(
    client, test_db_comments, mock_comment_data, user_token_2
):
    response = client.patch(
        f"{API_PREFIX}/1/comments/1/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_2}"},
    )
    validate_error(response, 403, "Access denied")


def test_update_comment_post_not_found(
    client, test_db_user, mock_comment_data, user_token_1
):
    response = client.patch(
        f"{API_PREFIX}/999/comments/1/",
        json=mock_comment_data,
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Post not found")


def test_delete_comment(client, test_db_comment, user_token_1):
    response = client.delete(
        f"{API_PREFIX}/1/comments/1/",
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_delete_comment_not_found(client, test_db_comment, user_token_1):
    response = client.delete(
        f"{API_PREFIX}/1/comments/999/",
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Comment not found")


def test_delete_comment_post_not_found(
    client, test_db_user, mock_comment_data, user_token_1
):
    response = client.delete(
        f"{API_PREFIX}/999/comments/1/",
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    validate_error(response, 404, "Post not found")


def test_delete_comment_access_denied(client, test_db_comments, user_token_2):
    response = client.delete(
        f"{API_PREFIX}/1/comments/1/",
        headers={"Authorization": f"Bearer {user_token_2}"},
    )
    validate_error(response, 403, "Access denied")


def test_get_comments_statistics(client, test_db_comments, user_token_1):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    response = client.get(
        f"{API_PREFIX}/1/comments-daily-breakdown?date_from={today}&date_to={tomorrow}",
        headers={"Authorization": f"Bearer {user_token_1}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["date"] == today.isoformat()
    assert data[0]["total_comments"] == 4
    assert data[0]["banned_comments"] == 2
