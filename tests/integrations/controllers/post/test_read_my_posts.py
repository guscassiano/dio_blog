import pytest
from fastapi import status
from httpx import AsyncClient


async def test_read_posts_by_status_sucess(
    client: AsyncClient, access_token: str, populate_posts
):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/me", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    for item in response.json():
        assert item["author_nickname"] == "test_user"
