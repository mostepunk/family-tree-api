from typing import Any
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from family.adapters.db.models.base import BaseTable
from family.adapters.schemas.base import BaseSchema


class BaseCRUD:
    @property
    def _table(self):
        return BaseTable

    @property
    def _out(self):
        return BaseSchema

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update(self, table_uuid: UUID, upd_dict: dict[str, Any]) -> BaseTable:
        query = (
            update(self._table)
            .where(self._table.uuid == table_uuid)
            .values(upd_dict)
            .returning(self._table)
        )
        res = await self.session.scalar(query)
        if res:
            return self._out.model_validate(res)
        return None

    async def create(self, table_dict: dict[str, Any]):
        query = insert(self._table).values(table_dict).returning(self._table)
        res = await self.session.scalar(query)
        return self._out.model_validate(res)
