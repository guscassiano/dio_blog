import asyncio
import os
import sys
from pathlib import Path

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Adicionar o diretório raiz do projeto ao path para que os imports funcionem
sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ.setdefault("DATABASE_URL", f"sqlite:///tests.db")


@pytest_asyncio.fixture
async def db(request):
    from src.database import database, engine, metadata

    await database.connect()
    metadata.create_all(engine)

    yield

    # Teardown: limpar dados e desconectar
    metadata.drop_all(engine)
    await database.disconnect()


@pytest_asyncio.fixture
async def client(db):
    from src.main import app

    transport = ASGITransport(app=app)
    headers = {
        "access_token": "application/json",
        "Content-Type": "application/json",
    }
    async with AsyncClient(base_url="https://test", transport=transport, headers=headers) as client:
        yield client


@pytest_asyncio.fixture
async def access_token(client: AsyncClient):
    response = await client.post("/auth/login", json={"user_id": 1})
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def populate_posts(db):
    from src.schemas.post import PostIn
    from src.services.post import PostService

    service = PostService()
    await service.create(PostIn(title="post 1", content="some content", published=True))
    await service.create(PostIn(title="post 2", content="some content", published=True))
    await service.create(PostIn(title="post 3", content="some content", published=False))
