from fastapi import status
from httpx import AsyncClient


async def test_read_all_users_success(
    client: AsyncClient, test_user: dict, second_user_token: str
):
    headers = {"Authorization": f"Bearer {second_user_token}"}
    response = await client.get(f"/users", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    print(data)
    assert data[0]["nickname"] == "test_user"
    assert "email" not in data
    assert "created_at" not in data


async def test_read_all_users_without_token(client: AsyncClient):
    response = await client.get(f"/users")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid authorization code."
