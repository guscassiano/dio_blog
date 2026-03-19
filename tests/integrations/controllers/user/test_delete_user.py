from fastapi import status
from httpx import AsyncClient


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
