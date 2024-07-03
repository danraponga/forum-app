from app.core.security import create_access_token, create_refresh_token
from app.tests.conftest import test_users
from app.tests.error_validator import validate_error

API_PREFIX = "/api/auth"


async def test_sign_up(client, mock_user_data):
    response = await client.post(f"{API_PREFIX}/sign_up/", json=mock_user_data)
    assert response.status_code == 200

    data = response.json()
    assert data["user"]["email"] == mock_user_data["email"]
    assert data["user"]["username"] == mock_user_data["username"]
    assert "access_token" in data["tokens"]
    assert "refresh_token" in data["tokens"]


async def test_sign_up_existing_user(client, mock_user_data):
    response = await client.post(f"{API_PREFIX}/sign_up/", json=mock_user_data)
    assert response.status_code == 200

    response = await client.post(f"{API_PREFIX}/sign_up/", json=mock_user_data)
    validate_error(response, 409, "User with this email already exists")


async def test_sign_up_invalid_data(client, mock_user_data):
    mock_data = mock_user_data.copy()
    mock_data["email"] = "WrongEmailFormat"
    response = await client.post(f"{API_PREFIX}/sign_up/", json=mock_data)
    assert response.status_code == 422

    mock_data = mock_user_data.copy()
    mock_data["username"] = "abc"
    response = await client.post(f"{API_PREFIX}/sign_up/", json=mock_data)
    assert response.status_code == 422

    mock_data = mock_user_data.copy()
    mock_data["password"] = "123"
    response = await client.post(f"{API_PREFIX}/sign_up/", json=mock_data)
    assert response.status_code == 422


async def test_sign_in(client, mock_login_data, mock_user_data):
    await client.post(f"{API_PREFIX}/sign_up/", json=mock_user_data)
    response = await client.post(f"{API_PREFIX}/login/", json=mock_login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"


async def test_sign_in_invalid_credentials(client):
    response = await client.post(
        f"{API_PREFIX}/login/",
        json={"email": "wrong@email.com", "password": "wrongpassword"},
    )
    validate_error(response, 401, "Invalid credentials")


async def test_me(client, test_db_user):
    token = create_access_token(1)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get(f"{API_PREFIX}/me/", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == test_users[0]["email"]
    assert data["username"] == test_users[0]["username"]


async def test_me_invalid_token(client):
    token = create_refresh_token(1)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get(f"{API_PREFIX}/me/", headers=headers)
    validate_error(response, 401, "Invalid token type")


async def test_me_invalid_credentials(client):
    headers = {"Authorization": "Bearer invalidcredentials"}

    response = await client.get(f"{API_PREFIX}/me/", headers=headers)
    validate_error(response, 401, "Invalid credentials")


async def test_me_not_authorized(client):
    response = await client.get(f"{API_PREFIX}/me/", headers={})
    validate_error(response, 401, "Not authorized")


async def test_me_not_found(client):
    token = create_access_token(1)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get(f"{API_PREFIX}/me/", headers=headers)
    validate_error(response, 404, "User not found")


async def test_refresh_token(client, test_db_user):
    token = create_refresh_token(1)

    response = await client.post(
        f"{API_PREFIX}/refresh/", json={"refresh_token": token}
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data


async def test_refresh_token_invalid_token(client):
    token = create_access_token(1)

    response = await client.post(
        f"{API_PREFIX}/refresh/", json={"refresh_token": token}
    )
    validate_error(response, 401, "Invalid token type")


async def test_refresh_token_not_found(client):
    token = create_refresh_token(1)

    response = await client.post(
        f"{API_PREFIX}/refresh/", json={"refresh_token": token}
    )
    validate_error(response, 404, "User not found")
