import pytest
from httpx import AsyncClient

from fastapi import status


@pytest.mark.parametrize("published,total", [("on", 2), ("off", 1)])
async def test_read_posts_by_status_sucess(client: AsyncClient, access_token: str, populate_posts, published: str, total: int):
    params = {"published": published, "limit": 10}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params=params, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == total


async def test_read_posts_limit_success(client: AsyncClient, access_token: str, populate_posts):
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


async def test_read_posts_empty_parameters_fail(client: AsyncClient, access_token: str, populate_posts):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params={}, headers=headers)

    content = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert content["detail"][0]["loc"] == ["query", "published"]
    assert content["detail"][1]["loc"] == ["query", "limit"]
