from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from fastapi.security import SecurityScopes
from pydantic import validator

from family.adapters.schemas.base import BaseDBSchema, BaseSchema


class Roles(str, Enum):
    superadmin: str = "ROOT"
    all_access: str = "ADMIN"
    it_staff: str = "IT_SUPPORT"
    read: str = "READ"
    write: str = "WRITE"


class AccountSchema(BaseSchema):
    uuid: UUID
    username: str
    email: str
    is_enable: bool = True
    roles: list[str]

    def is_superadmin(self):
        return Roles.superadmin in self.roles

    def is_it_staff(self):
        return Roles.it_staff in self.roles

    def is_superadmin_or_it_staff(self):
        return any((self.is_superadmin(), self.is_it_staff()))

    def is_all_access(self):
        return Roles.all_access.value in self.roles

    def has_access(self, security_scopes: SecurityScopes):
        return any(role in self.roles for role in security_scopes.scopes)


class AccountDBSchema(AccountSchema, BaseDBSchema):
    last_visit: datetime | None
    hashed_password: str

    @validator("roles", pre=True)
    @classmethod
    def validate_roles(cls, role):
        return [role.name]
