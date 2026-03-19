import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize("published, total", [("on", 2), ("off", 1)])
async def test_read_posts_by_status_sucess(
    client: AsyncClient, access_token: str, published: str, total: int, populate_posts
):
    params = {"published": published, "limit": 10}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/me", params=params, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    for item in response.json():
        assert item["author_nickname"] == "test_user"
