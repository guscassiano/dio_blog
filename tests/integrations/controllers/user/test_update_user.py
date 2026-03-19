from fastapi import status
from httpx import AsyncClient


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
