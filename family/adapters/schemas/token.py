from __future__ import annotations

from datetime import datetime

from family.adapters.schemas.accounts import RoleSchema
from family.adapters.schemas.base import BaseSchema


class Token(BaseSchema):
    user_name: str
    email: str | None
    role: RoleSchema
    exp: datetime | None = None
