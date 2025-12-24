from httpx import AsyncClient

from fastapi import status


async def test_login_success(client: AsyncClient):
    data = {"user_id": 1}

    response = await client.post("/auth/login", json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] is not None
