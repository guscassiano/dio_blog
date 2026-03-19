from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import auth, post, user
from src.database import database
from src.expections import ForbiddenPostError, NotFoundPostError


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    },
    {
        "name": "User",
        "description": "User operations.",
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
    version="1.0.3",
    description="""
Blog API to help you create a personal blog. 🚀

## Posts

You will be able:

* **Read all posts**
* **Create posts**
* **Read only the user's posts**
* **Read posts by id**
* **Update posts**
* **Delete posts**

## Users

You will be able:

* **Create users**
* **Read the user's own**
* **Read users by id**
* **Update users**
* **Delete users**
* **Read all users**
""",
    summary="Personal blog API. To created, read, update and delete users and posts.",
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
app.include_router(user.router, tags=["User"])


@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(ForbiddenPostError)
async def not_found_post_exception_handler(request: Request, exc: ForbiddenPostError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
