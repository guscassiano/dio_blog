from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from src.schemas.auth import ForgotPasswordIn, LoginIn, ResetPasswordIn
from src.security import (
    create_password_reset_token,
    sign_jwt,
    verify_password_reset_token,
)
from src.services.email import send_reset_password_email
from src.services.user import UserService
from src.views.auth import LoginOut

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginOut)
async def login(data: LoginIn):
    """Login with email and password"""
    user = await UserService.get_user_by_email(data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    if not UserService.verify_password(data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    return await sign_jwt(user_id=user["id"], role=user["role"])


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(data: ForgotPasswordIn, background_tasks: BackgroundTasks):
    """Generates the token and simulates sending an email"""
    user = await UserService.get_user_by_email(data.email)

    if user:
        token = create_password_reset_token(email=data.email)

        background_tasks.add_task(send_reset_password_email, data.email, token)

    return {"message": "If the email is registrered, a password token has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetPasswordIn):
    """Receive the token, validate and change the password at the bank"""
    email = verify_password_reset_token(data.token)
    print(email)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired reset token.",
        )

    user = await UserService.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await UserService.update_password(user["id"], data.new_password)
    return {"message": "Password updated successfully."}
