from __future__ import annotations

from datetime import datetime

from family.adapters.schemas.base import BaseSchema


class Token(BaseSchema):
    username: str
    email: str | None
    roles: list[str]
    exp: datetime | None
