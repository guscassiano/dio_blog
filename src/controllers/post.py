from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.post import PostIn, PostUpdateIn
from src.security import login_required
from src.services.post import PostService
from src.views.post import PostCreateOut, PostOut, PostOutDetail

router = APIRouter(prefix="/posts", dependencies=[Depends(login_required)])
service = PostService()


@router.get("/", response_model=list[PostOut])
async def read_posts(
    published: bool = True,
    limit: int = 10,
    skip: int = 0,
):
    return await service.read_all(published=published, limit=limit, skip=skip)


@router.get("/me", response_model=list[PostOutDetail])
async def read_my_posts(
    current_user: Annotated[dict, Depends(login_required)],
    limit: int = 10,
    skip: int = 0,
):
    return await service.read_me(
        user_id=current_user["user_id"], limit=limit, skip=skip
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostCreateOut)
async def create_post(
    post: PostIn, current_user: Annotated[dict, Depends(login_required)]
):
    user_id = int(current_user["user_id"])
    return {
        **post.model_dump(),
        "id": await service.create(post, user_id),
        "user_id": user_id,
    }


@router.get("/{id}", response_model=PostOutDetail)
async def read_post(id: int):
    return await service.read(id)


@router.patch("/{id}", response_model=PostOutDetail)
async def update_post(
    id: int, post: PostUpdateIn, current_user: Annotated[dict, Depends(login_required)]
):
    return await service.update(id, post, current_user["user_id"], current_user["role"])


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, current_user: Annotated[dict, Depends(login_required)]):
    await service.delete(id, current_user["user_id"], current_user["role"])
