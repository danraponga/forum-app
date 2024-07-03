from app.tests.conftest import test_users

API_PREFIX = "/api/users"


async def test_read_users_all(client, test_db_users):
    response = await client.get(f"{API_PREFIX}/")
    assert response.status_code == 200

    data = response.json()
    assert "users" in data
    assert data["total"] == 2
    assert data["users"][0]["email"] == test_users[0]["email"]
    assert data["users"][1]["email"] == test_users[1]["email"]


async def test_read_user(client, test_db_user):
    response = await client.get(f"{API_PREFIX}/{test_db_user.id}/")
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == test_db_user.email


async def test_read_user_not_found(client):
    response = await client.get(f"{API_PREFIX}/9999/")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"
