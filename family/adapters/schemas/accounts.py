from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import ConfigDict

from family.adapters.schemas.base import BaseDBSchema, BaseSchema
from family.resources.role_map import (
    ADMIN,
    ADMIN_LEVEL,
    MODERATOR,
    MODERATOR_LEVEL,
    NONE,
    NONE_LEVEL,
    READ,
    WRITE,
    WRITE_LEVEL,
)


class _AccountDBSchema(_AccountSchema, BaseDBSchema):
    last_visit: datetime | None
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class Roles(str, Enum):
    guest: str = NONE
    read: str = READ
    write: str = WRITE
    moderator: str = MODERATOR
    admin: str = ADMIN


class RoleSchema(BaseSchema):
    level: int
    name: str


class AccountSchema(BaseSchema):
    user_name: str
    email: str
    role: RoleSchema

    @property
    def is_admin(self):
        return self.role.level == ADMIN_LEVEL

    @property
    def is_moderator(self):
        return self.role.level == MODERATOR_LEVEL

    @property
    def can_read(self):
        return self.role.level < NONE_LEVEL

    @property
    def can_write(self):
        return self.role.level < WRITE_LEVEL
