from httpx import AsyncClient

from fastapi import status


async def test_read_post_success(client: AsyncClient, access_token: str, populate_posts):
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 1

    response = await client.get(f"/posts/{post_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == post_id


async def test_read_post_not_authenticated_fail(client: AsyncClient, populate_posts):
    post_id = 1

    response = await client.get(f"/posts/{post_id}", headers={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid authorization code."


async def test_read_post_not_found_fail(client: AsyncClient, access_token: str, populate_posts):
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 4

    response = await client.get(f"/posts/{post_id}", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Post not found"
