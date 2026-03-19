from fastapi import status
from httpx import AsyncClient


async def test_get_user_by_id_hides_email(
    client: AsyncClient, test_user: dict, access_token: str
):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get(f"/users/{test_user["id"]}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["nickname"] == "test_user"
    assert "email" not in data
    assert "created_at" not in data


async def test_get_user_by_id_without_token(client: AsyncClient):
    response = await client.get(f"/users/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid authorization code."
