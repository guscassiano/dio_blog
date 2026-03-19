from fastapi import status
from httpx import AsyncClient


async def test_get_user_me(client: AsyncClient, access_token: str, test_user: dict):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/users/me", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user["email"]
    assert "created_at" in data
