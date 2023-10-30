from datetime import datetime
from typing import NoReturn
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from family.adapters.db.crud.base import BaseCRUD
from family.adapters.db.models import AccountModel
from family.adapters.schemas.accounts import AccountDBSchema


class AccountCRUD(BaseCRUD):
    @property
    def _table(self):
        return AccountModel

    @property
    def _out(self):
        return AccountDBSchema

    async def get_by_username(self, username: str):
        query = (
            select(self._table).where(self._table.user_name == username)
            # .options(joinedload(self._table.role))
        )
        res = await self.session.scalar(query)
        return self._out.model_validate(res)

    async def update_user_last_visit(self, user_uuid: UUID) -> NoReturn:
        query = (
            update(self._table)
            .where(self._table.uuid == user_uuid)
            .values({"last_visit": datetime.now()})
            .options(selectinload(self._table.role))
            .returning(self._table)
        )
        res = await self.session.scalar(query)
        return self._out.model_validate(res)
