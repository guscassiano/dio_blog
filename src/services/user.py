from datetime import datetime

import bcrypt

from src.database import database
from src.models.user import users


class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        pwd_bytes = password.encode("utf-8")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)

        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        password_bytes = plain_password.encode("utf-8")
        hashed_password_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(password_bytes, hashed_password_bytes)

    @staticmethod
    async def update_password(user_id: int, new_password: str):
        hashed_password = UserService.hash_password(new_password)

        command = (
            users.update().where(users.c.id == user_id).values(password=hashed_password)
        )
        await database.execute(command)

    @staticmethod
    async def create_user(name: str, email: str, nickname: str, password: str):
        hashed_password = UserService.hash_password(password)
        query = users.insert().values(
            name=name,
            email=email,
            nickname=nickname,
            password=hashed_password,
            created_at=datetime.now(),
            active=True,
        )
        return await database.execute(query)

    @staticmethod
    async def get_user_by_id(user_id: int):
        query = users.select().where(users.c.id == user_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_user_by_email(email: str):
        query = users.select().where(users.c.email == email)
        return await database.fetch_one(query)

    @staticmethod
    async def get_user_by_nickname(nickname: str):
        query = users.select().where(users.c.nickname == nickname)
        return await database.fetch_one(query)

    @staticmethod
    async def get_all_users():
        query = users.select()
        return await database.fetch_all(query)

    @staticmethod
    async def update_user(
        user_id: int, name: str = None, email: str = None, nickname: str = None
    ):
        values = {}
        if name:
            values["name"] = name
        if email:
            values["email"] = email
        if nickname:
            values["nickname"] = nickname

        if not values:
            return await UserService.get_user_by_id(user_id)

        query = users.update().where(users.c.id == user_id).values(**values)
        await database.execute(query)
        return await UserService.get_user_by_id(user_id)

    @staticmethod
    async def deactivate_user(user_id: int):
        query = users.update().where(users.c.id == user_id).values(active=False)
        return await database.execute(query)

    @staticmethod
    async def toggle_user_status(user_id: int):
        user = await UserService.get_user_by_id(user_id)
        if not user:
            return None
        query = (
            users.update().where(users.c.id == user_id).values(active=not user.active)
        )
        await database.execute(query)
        return await UserService.get_user_by_id(user_id)
