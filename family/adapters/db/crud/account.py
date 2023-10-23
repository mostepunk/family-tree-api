from datetime import datetime
from typing import NoReturn
from uuid import UUID

from loguru import logger as logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from family.adapters.db.crud.base import BaseCRUD
from family.adapters.db.models import AccountModel, RoleModel
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
            select(self._table)
            .where(self._table.username == username)
            .options(selectinload(self._table.roles))
        )
        res = await self.session.scalar(query)
        logging.info(f"Found User: {res}")
        logging.info(f"USER Role: {res.roles}")
        return self._out.from_orm(res)

    async def update_user_last_visit(self, user_uuid: UUID) -> NoReturn:
        # return await self.update(user_uuid, {"last_visit": moscow_now()})
        return await self.update(user_uuid, {"last_visit": datetime.now()})

    async def get_role_uuid(self, role_name: str) -> UUID:
        query = select(RoleModel.uuid).where(RoleModel.name == role_name)
        return (await self.session.scalar(query)).first()
