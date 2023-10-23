from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from family.adapters.db.models.base import BaseTable


class AccountModel(BaseTable):
    __tablename__ = "accounts"

    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.uuid")
    )
    last_visit: Mapped[datetime | None] = mapped_column(DateTime)
    person_uuid: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True))

    roles: Mapped[list["RoleModel"]] = relationship(
        back_populates="accounts", lazy=selectinload
    )


class RoleModel(BaseTable):
    """
    чтение: просмотр древа
    запись включает в себя чтение + модификация дерева
    админ включает в себя чтение/запись + создать account
    рут включает в себя админ/чтение/запись + назначить админом

    3 read
     2 write
      1 admin, it_staff
       0 root
    """

    __tablename__ = "roles"
    __table_args__ = (UniqueConstraint("level", "name"), {})

    level: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(10), unique=True)

    accounts: Mapped[list["AccountModel"] | None] = relationship(back_populates="roles")
