from fastapi import status
from httpx import AsyncClient


async def test_update_post_success(
    client: AsyncClient, access_token: str, populate_posts
):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"title": "update title post 1"}
    post_id = 1

    response = await client.patch(f"/posts/{post_id}", json=data, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == data["title"]


async def test_update_post_not_authenticated_fail(client: AsyncClient, populate_posts):
    post_id = 1

    response = await client.patch(f"/posts/{post_id}", headers={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid authorization code."


async def test_update_post_not_found_fail(
    client: AsyncClient, access_token: str, populate_posts
):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"title": "update title post 1"}
    post_id = 4

    response = await client.patch(f"/posts/{post_id}", json=data, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Post not found"


async def test_update_post_by_other_user(
    client: AsyncClient, second_user_token: str, populate_posts
):
    headers = {"Authorization": f"Bearer {second_user_token}"}
    data = {"title": "update title post 1"}
    post_id = 1

    response = await client.patch(f"/posts/{post_id}", json=data, headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "You don't have permission to update this post"
