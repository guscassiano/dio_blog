import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_login_success(client: AsyncClient, test_user: dict):
    data = {"email": test_user["email"], "password": test_user["password"]}

    response = await client.post("/auth/login", json=data)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["access_token"] is not None


async def test_login_wrong_password(client: AsyncClient):
    data = {"email": "gu@example.com", "password": "senha_errada_123"}

    response = await client.post("/auth/login", json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password"


async def test_login_nonexistent_user(client: AsyncClient):
    data = {"email": "fantasma@example.com", "password": "qualquersenha"}

    response = await client.post("/auth/login", json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_forgot_password_success(client: AsyncClient):
    data = {"email": "user@example.com"}

    response = await client.post("/auth/forgot-password", json=data)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert "token has been sent" in response.json()["message"]


async def test_reset_password_invalid_token(client: AsyncClient):
    data = {"token": "um_token_jwt_inventado_e_falso", "new_password": "NovaSenha123!"}

    response = await client.post("/auth/reset-password", json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid or expired" in response.json()["detail"]
