from contextlib import asynccontextmanager

from src.controllers import auth, post
from src.database import database, engine, metadata

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.models.post import posts

    metadata.create_all(engine)
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post.router)
app.include_router(auth.router)
