from httpx import AsyncClient

from fastapi import status


async def test_create_post_success(client: AsyncClient, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "title": "new post 1",
        "content": "some content",
        "published_at": "2025-12-22T22:03:00.000Z",
        "published": True,
    }

    response = await client.post("/posts/", json=data, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] is not None


async def test_create_post_invalid_payload_fail(client: AsyncClient, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "content": "some content",
        "published_at": "2025-12-22T22:03:00.000Z",
        "published": True,
    }

    response = await client.post("/posts/", json=data, headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


async def test_create_post_not_authenticated_fail(client: AsyncClient):
    data = {
        "content": "some content",
        "published_at": "2025-12-22T22:03:00.000Z",
        "published": True,
    }

    response = await client.post("/posts/", json=data, headers={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid authorization code."
