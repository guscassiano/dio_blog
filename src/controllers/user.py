from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.user import UserCreate, UserRead, UserUpdate
from src.security import get_current_user, login_required
from src.services.user import UserService
from src.views.user import UserReadMeView, UserReadView

router = APIRouter(prefix="/users", tags=["User"])


@router.post(
    "/register", response_model=UserReadMeView, status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    existing_email = await UserService.get_user_by_email(user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    existing_nickname = await UserService.get_user_by_nickname(user_data.nickname)
    if existing_nickname:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Nickname already taken"
        )

    user_id = await UserService.create_user(
        name=user_data.name,
        email=user_data.email,
        nickname=user_data.nickname,
        password=user_data.password,
    )

    user = await UserService.get_user_by_id(user_id)
    return user


@router.get("/me", response_model=UserReadMeView)
async def get_current_user_info(current_user: Annotated[dict, Depends(login_required)]):
    """Get current authenticated user info"""
    user = await UserService.get_user_by_id(int(current_user["user_id"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get(
    "/{user_id}", response_model=UserReadView, dependencies=[Depends(login_required)]
)
async def get_user(user_id: int):
    """Get user by ID"""
    user = await UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get(
    "", response_model=list[UserReadView], dependencies=[Depends(login_required)]
)
async def list_users():
    """List all users"""
    return await UserService.get_all_users()


@router.put("/{user_id}", response_model=UserReadMeView)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: Annotated[dict, Depends(login_required)],
):
    """Update user (only owner or admin)"""
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile",
        )

    user = await UserService.update_user(
        user_id=user_id,
        name=user_data.name,
        email=user_data.email,
        nickname=user_data.nickname,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: int, current_user: Annotated[dict, Depends(login_required)]
):
    """Delete user (only owner)"""
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only deactivate your own account",
        )

    result = await UserService.deactivate_user(user_id)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.patch("/{id}/status", status_code=status.HTTP_200_OK)
async def toggle_status_for_admin(
    id: int, current_user: Annotated[dict, Depends(login_required)]
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can suspend/restore accounts.",
        )

    user = await UserService.toggle_user_status(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {"detail": f"Active status for user '{user.name}' successfully changed!"}
