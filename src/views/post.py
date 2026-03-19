from pydantic import AwareDatetime, BaseModel, NaiveDatetime


class PostCreateOut(BaseModel):
    id: int
    title: str
    content: str
    published_at: AwareDatetime | NaiveDatetime | None
    published: bool
    user_id: int


class PostOut(BaseModel):
    id: int
    title: str
    content: str


class PostOutDetail(BaseModel):
    id: int
    title: str
    content: str
    published_at: AwareDatetime | NaiveDatetime | None
    author_nickname: str
