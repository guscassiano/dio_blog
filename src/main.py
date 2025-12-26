from contextlib import asynccontextmanager

from src.expections import NotFoundPostError
from src.controllers import auth, post
from src.database import database, engine, metadata

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

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

@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )