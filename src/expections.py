from http import HTTPStatus


class NotFoundPostError(Exception):
    def __init__(
        self, message: str = "Post not found", status_code: int = HTTPStatus.NOT_FOUND
    ) -> None:
        self.message = message
        self.status_code = status_code


class ForbiddenPostError(Exception):
    def __init__(self, message: str, status_code: int = HTTPStatus.FORBIDDEN) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
