from __future__ import annotations

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from family.adapters.db.models.base import Base
from family.resources.role_map import ROLE_LEVEL_MAP


class AccountModel(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(32), unique=True)
    real_name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(128))

    ft_settings: Mapped[list["AccountFTSettings"]] = relationship(
        back_populates="account",
        uselist=True,
        lazy="selectin",
    )
    app_settings: Mapped[list["AccountSettings"]] = relationship(
        back_populates="account",
        uselist=True,
        lazy="selectin",
    )
    role_settings: Mapped["AccountFTSettings"] = relationship(
        uselist=False,
        primaryjoin="and_(AccountModel.user_id == AccountFTSettings.user_id,  AccountFTSettings.setting_name == 'canedit')",
        lazy="selectin",
        viewonly=True,
    )

    @property
    def role(self):
        role_name = self.role_settings.setting_value
        return {"level": ROLE_LEVEL_MAP.get(role_name), "name": role_name}


class AccountFTSettings(Base):
    __tablename__ = "user_gedcom_setting"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "gedcom_id", "setting_name"),
        {},
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    gedcom_id: Mapped[int] = mapped_column(ForeignKey("gedcom.gedcom_id"), index=True)
    setting_name: Mapped[str] = mapped_column(String(32), unique=True)
    setting_value: Mapped[str] = mapped_column(String(255))

    account: Mapped["AccountModel"] = relationship(back_populates="ft_settings")


class AccountSettings(Base):
    __tablename__ = "user_setting"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "setting_name"),
        {},
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    setting_name: Mapped[str] = mapped_column(String(32), unique=True)
    setting_value: Mapped[str] = mapped_column(String(255))

    account: Mapped["AccountModel"] = relationship(back_populates="app_settings")
