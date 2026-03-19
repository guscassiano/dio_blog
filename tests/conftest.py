import sys
import time
from pathlib import Path

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Adicionar o diretório raiz do projeto ao path para que os imports funcionem
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings

settings.database_url = "sqlite:///tests.db"


@pytest_asyncio.fixture
async def db(request):
    from src.database import database, engine, metadata
    from src.models.post import posts
    from src.models.user import users

    await database.connect()
    metadata.create_all(engine)

    yield database

    # Teardown: limpar dados e desconectar
    metadata.drop_all(engine)
    await database.disconnect()


@pytest_asyncio.fixture
async def client(db):
    from src.main import app

    transport = ASGITransport(app=app)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    async with AsyncClient(
        base_url="http://test", transport=transport, headers=headers
    ) as client:
        yield client


@pytest_asyncio.fixture
async def test_user(db):
    from src.models.user import users
    from src.services.user import UserService

    hashed_pw = UserService.hash_password("123456")

    query = users.insert().values(
        name="Test User",
        nickname="test_user",
        email="user@example.com",
        password=hashed_pw,
        active=True,
        role="admin",
    )
    user_id = await db.execute(query)
    return {"id": user_id, "email": "user@example.com", "password": "123456"}


@pytest_asyncio.fixture
async def access_token(client: AsyncClient, test_user: dict):
    response = await client.post(
        "/auth/login",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def second_user(client: AsyncClient, db):
    response = await client.post(
        "/users/register",
        json={
            "name": "User Two",
            "email": "user2@example.com",
            "nickname": "usertwo",
            "password": "password123",
        },
    )

    user = response.json()
    user["password"] = "password123"

    return user


@pytest_asyncio.fixture
async def second_user_token(client: AsyncClient, second_user: dict):
    response = await client.post(
        "/auth/login",
        json={"email": second_user["email"], "password": second_user["password"]},
    )
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def populate_posts(db, test_user: dict):
    from src.schemas.post import PostIn
    from src.services.post import PostService

    service = PostService()
    await service.create(
        PostIn(
            title="post 1",
            content="some content",
            published_at=time.time(),
            published=True,
        ),
        user_id=test_user["id"],
    )
    await service.create(
        PostIn(
            title="post 2",
            content="some content",
            published_at=time.time(),
            published=True,
        ),
        user_id=test_user["id"],
    )
    await service.create(
        PostIn(
            title="post 3",
            content="some content",
            published_at=time.time(),
            published=False,
        ),
        user_id=test_user["id"],
    )
