import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_user_success(client: AsyncClient):
    """Test successful user registration"""
    response = await client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "nickname": "testuser",
            "password": "securepass123",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["nickname"] == "testuser"
    assert "password" not in data


async def test_register_user_duplicate_email(client: AsyncClient):
    """Test registration with duplicate email"""
    await client.post(
        "/users/register",
        json={
            "name": "User One",
            "email": "duplicate@example.com",
            "nickname": "userone",
            "password": "password123",
        },
    )

    response = await client.post(
        "/users/register",
        json={
            "name": "User Two",
            "email": "duplicate@example.com",
            "nickname": "usertwo",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already registered" in response.json()["detail"]


async def test_register_user_without_email(client: AsyncClient):
    """Test registration without email"""
    response = await client.post(
        "/users/register",
        json={
            "name": "User Two",
            "email": "",
            "nickname": "usertwo",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert (
        "value is not a valid email address: An email address must have an @-sign."
        in response.json()["detail"][0]["msg"]
    )


async def test_get_user_me(client: AsyncClient, access_token: str, test_user: dict):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/users/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert "created_at" in data


async def test_get_user_by_id_hides_email(
    client: AsyncClient, test_user: dict, access_token: str
):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get(f"/users/{test_user["id"]}", headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert data["nickname"] == "test_user"
    assert "email" not in data
    assert "created_at" not in data


async def test_get_user_by_id_without_token(client: AsyncClient):
    response = await client.get(f"/users/1")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authorization code."


async def test_update_users_by_id_success(
    client: AsyncClient, test_user: dict, access_token: str
):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.put(
        f"/users/{test_user["id"]}",
        headers=headers,
        json={
            "name": "Test User Update",
            "email": "user@example.com",
            "nickname": "test_user",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["name"] == "Test User Update"
    assert data["email"] == test_user["email"]


async def test_update_user_by_id_without_correct_token(
    client: AsyncClient, test_user: dict, access_token: str
):
    response = await client.post(
        "/users/register",
        json={
            "name": "Test User Example",
            "email": "test@example.com",
            "nickname": "testuser",
            "password": "securepass123",
        },
    )

    data = response.json()
    update_response = await client.put(
        f"/users/{data["id"]}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "Test User Update",
            "email": "user@example.com",
            "nickname": "test_user",
        },
    )

    assert update_response.status_code == status.HTTP_403_FORBIDDEN
    assert update_response.json()["detail"] == "You can only update your own profile"


async def test_delete_user_by_id_success(
    client: AsyncClient, test_user: dict, access_token: str
):
    header = {"Authorization": f"Bearer {access_token}"}
    response = await client.delete(f"/users/{test_user['id']}", headers=header)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response_login = await client.post(
        f"/auth/login", json={"email": "user@example.com", "password": "123456"}
    )

    assert response_login.status_code == status.HTTP_403_FORBIDDEN
    assert response_login.json()["detail"] == "User account is inactive"


async def test_delete_user_by_id_without_correct_token(
    client: AsyncClient, test_user: dict, access_token: str
):
    response = await client.post(
        "/users/register",
        json={
            "name": "Test User Example",
            "email": "test@example.com",
            "nickname": "testuser",
            "password": "securepass123",
        },
    )

    data = response.json()
    delete_response = await client.delete(
        f"/users/{data["id"]}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert delete_response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        delete_response.json()["detail"] == "You can only deactivate your own account"
    )
