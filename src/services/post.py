from databases.interfaces import Record
from sqlalchemy import select

from src.database import database
from src.expections import ForbiddenPostError, NotFoundPostError
from src.models.post import posts
from src.models.user import users
from src.schemas.post import PostIn, PostUpdateIn


class PostService:
    async def read_all(
        self, published: bool, limit: int, skip: int = 0
    ) -> list[Record]:
        query = (
            select(
                posts.c.id,
                posts.c.title,
                posts.c.content,
                posts.c.published_at,
                posts.c.published,
                users.c.nickname.label("author_nickname"),
            )
            .select_from(posts.join(users, posts.c.user_id == users.c.id))
            .where(posts.c.published == published)
            .limit(limit)
            .offset(skip)
        )
        return await database.fetch_all(query)

    async def read_me(self, user_id, limit: int, skip: int = 0) -> list[Record]:
        query = (
            select(
                posts.c.id,
                posts.c.title,
                posts.c.content,
                posts.c.published_at,
                users.c.nickname.label("author_nickname"),
            )
            .select_from(posts.join(users, posts.c.user_id == users.c.id))
            .where(posts.c.user_id == user_id)
            .limit(limit)
            .offset(skip)
        )
        return await database.fetch_all(query)

    async def create(self, post: PostIn, user_id: int) -> int:
        command = posts.insert().values(
            title=post.title,
            content=post.content,
            published_at=post.published_at,
            published=post.published,
            user_id=user_id,
        )
        return await database.execute(command)

    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def update(
        self, id: int, post: PostUpdateIn, user_id: int, role: str
    ) -> Record:
        current_post = await self.__get_by_id(id)
        if not current_post:
            raise NotFoundPostError

        if current_post._mapping["user_id"] != user_id and role != "admin":
            raise ForbiddenPostError(
                message="You don't have permission to update this post"
            )

        data = post.model_dump(exclude_unset=True)

        command = posts.update().where(posts.c.id == id).values(**data)
        await database.execute(command)

        return await self.__get_by_id(id)

    async def delete(self, id: int, user_id: int, role: str) -> None:
        post = await self.__get_by_id(id)

        if post._mapping["user_id"] != user_id and role != "admin":
            raise ForbiddenPostError(
                message="You don't have permission to delete this post"
            )

        command = posts.delete().where((posts.c.id == id))
        await database.execute(command)

    async def count(self, id: int) -> int:
        query = "select count(id) as total from posts where id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total

    async def __get_by_id(self, id: int) -> Record:
        query = (
            select(
                posts.c.id,
                posts.c.title,
                posts.c.content,
                posts.c.published_at,
                posts.c.user_id,
                users.c.nickname.label("author_nickname"),
            )
            .select_from(posts.join(users, posts.c.user_id == users.c.id))
            .where(posts.c.id == id)
        )
        post = await database.fetch_one(query)
        if not post:
            raise NotFoundPostError
        return post
