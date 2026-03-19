import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize("published, total", [("on", 2), ("off", 1)])
async def test_read_posts_by_status_sucess(
    client: AsyncClient, access_token: str, published: str, total: int, populate_posts
):
    params = {"published": published, "limit": 10}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params=params, headers=headers)
    print(response.json(), total)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == total


async def test_read_posts_limit_success(
    client: AsyncClient, access_token: str, populate_posts
):
    params = {"published": "on", "limit": 1}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params=params, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


async def test_read_posts_not_authenticated_fail(client: AsyncClient, populate_posts):
    params = {"published": "on", "limit": 1}

    response = await client.get("/posts/", params=params, headers={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid authorization code."
