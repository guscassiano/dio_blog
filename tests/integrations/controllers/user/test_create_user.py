import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_user_success(client: AsyncClient):
    """Test successful user registration"""
    response = await client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "nickname": "testuser",
            "password": "securepass123",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["nickname"] == "testuser"
    assert "password" not in data


async def test_register_user_duplicate_email(client: AsyncClient):
    """Test registration with duplicate email"""
    await client.post(
        "/users/register",
        json={
            "name": "User One",
            "email": "duplicate@example.com",
            "nickname": "userone",
            "password": "password123",
        },
    )

    response = await client.post(
        "/users/register",
        json={
            "name": "User Two",
            "email": "duplicate@example.com",
            "nickname": "usertwo",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already registered" in response.json()["detail"]


async def test_register_user_without_email(client: AsyncClient):
    """Test registration without email"""
    response = await client.post(
        "/users/register",
        json={
            "name": "User Two",
            "email": "",
            "nickname": "usertwo",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert (
        "value is not a valid email address: An email address must have an @-sign."
        in response.json()["detail"][0]["msg"]
    )
