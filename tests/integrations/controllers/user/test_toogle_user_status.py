from fastapi import status
from httpx import AsyncClient


async def test_toogle_user_status_success(
    client: AsyncClient, second_user: dict, access_token: str
):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.patch(f"/users/{second_user["id"]}/status", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["detail"]
        == f"Active status for user '{second_user['name']}' successfully changed!"
    )


async def test_toogle_user_status_permission(
    client: AsyncClient, test_user: dict, second_user_token: str
):
    headers = {"Authorization": f"Bearer {second_user_token}"}
    response = await client.patch(f"/users/{test_user["id"]}/status", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        response.json()["detail"] == "Only administrators can suspend/restore accounts."
    )
