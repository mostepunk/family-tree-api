"""Схема для LoggingMiddleware."""

from typing import Optional

from pydantic import BaseModel, validator


class MWValidator(BaseModel):
    """Влидация данных для LoggingMiddleware."""

    request_body: Optional[str]
    response_body: Optional[str]
    url: Optional[str]

    @validator("request_body", "response_body", pre=True)
    def valid_body(cls, field):  # noqa N805
        """Валидация тела запроса.

        Args:
            field: ...

        Returns:
            str: ...
        """
        if isinstance(field, bytes):
            try:
                field = field.decode()
            except UnicodeDecodeError:
                field = "<file_bytes>"

            if field:
                return field
            else:
                return "<empty>"

        if isinstance(field, str):
            return field

    @validator("url", pre=True)
    def valid_url(cls, url) -> str:  # noqa N805
        """Переделывает параметры в более читаемый вид.

        http://127.0.0.1:8000/error?one=1&two=0
        ->
        http://127.0.0.1:8000/error params(one:1 two:0)

        Args:
            url: ...

        Returns:
            str: ...
        """
        if "?" in url:
            url = url.replace("?", " params(").replace("&", " ").replace("=", ":") + ")"
        return url
