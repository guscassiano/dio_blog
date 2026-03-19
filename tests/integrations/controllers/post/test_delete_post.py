from fastapi import status
from httpx import AsyncClient


async def test_delete_post_success(
    client: AsyncClient, access_token: str, populate_posts
):
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 1

    response = await client.delete(f"/posts/{post_id}", headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response_post = await client.get(f"/posts/{post_id}", headers=headers)

    assert response_post.status_code == status.HTTP_404_NOT_FOUND
    assert response_post.json()["detail"] == "Post not found"


async def test_delete_post_not_authenticated_fail(client: AsyncClient, populate_posts):
    post_id = 1

    response = await client.delete(f"/posts/{post_id}", headers={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid authorization code."


async def test_delete_post_role_user(
    client: AsyncClient, second_user_token: str, populate_posts
):
    headers = {"Authorization": f"Bearer {second_user_token}"}
    post_id = 1

    response = await client.delete(f"/posts/{post_id}", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "You don't have permission to delete this post"
