from contextlib import asynccontextmanager

from src.controllers import auth, post
from src.database import database, engine, metadata
from src.expections import NotFoundPostError

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.models.post import posts

    metadata.create_all(engine)
    await database.connect()
    yield
    await database.disconnect()


tags_metadata = [
    {
        "name": "Auth",
        "description": "Operations to authentication.",
    },
    {
        "name": "Post",
        "description": "Operations to keep posts.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

servers = [
    {"url": "http://localhost:8000", "description": "Staging environment"},
    {
        "url": "https://dio-blog-y7fj.onrender.com",
        "description": "Production environment",
    },
]

app = FastAPI(
    title="BlogAPI",
    version="1.0.2",
    description="""
Blog API to help you create a personal blog. 🚀

## Posts

You will be able:

* **Create posts**
* **Read posts by id**
* **Update posts**
* **Delete posts**
* **Limit quantity daily posts** (_not implemented_)
""",
    summary="Personal blog API. To created and read posts.",
    openapi_tags=tags_metadata,
    servers=servers,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router, tags=["Post"])
app.include_router(auth.router, tags=["Auth"])


@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
