from __future__ import annotations

from typing import NoReturn
from uuid import UUID

from loguru import logger as logging

from family.adapters.schemas.accounts import AccountDBSchema
from family.api.errors import CREDENTIALS_EXCEPTION
from family.services.base import BaseService
from family.utils.password import verify_password


class AccountService(BaseService):
    """AccountService."""

    async def authentiacate_user(
        self, username: str, password: str
    ) -> AccountDBSchema | None:
        """Authentiacate user.

        Args:
            username (str): username
            password (str): password

        Raises:
            CREDENTIALS_EXCEPTION: неправильный логин/пароль

        Returns:
            AccountDBSchema | None:
        """
        async with self.uow:
            account: AccountDBSchema = await self.uow.accounts.get_by_username(username)

        if not account:
            raise CREDENTIALS_EXCEPTION

        if not verify_password(password, account.hashed_password):
            raise CREDENTIALS_EXCEPTION

        logging.debug(f"User: {account.username} Logged In")
        await self.update_last_visit(account.uuid)
        return account

    async def update_last_visit(self, user_uuid: UUID) -> NoReturn:
        """Update last visit.

        Args:
            user_uuid (UUID): user_uuid
        """
        async with self.uow:
            account: AccountDBSchema = await self.uow.accounts.update_user_last_visit(
                user_uuid
            )
            await self.uow.commit()
            logging.debug(f"Updated Last Vist: {account.last_visit}")
