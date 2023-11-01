from sqlalchemy import select

from family.adapters.db.crud.base import BaseCRUD
from family.adapters.db.models import PersonModel
from family.adapters.schemas.persons import PersonDBSchema


class PersonCRUD(BaseCRUD):
    @property
    def _table(self):
        return PersonModel

    @property
    def _out(self):
        return PersonDBSchema

    async def get_by_id(self, person_id: str) -> PersonDBSchema:
        query = select(self._table).where(self._table.i_id == person_id)
        res = await self.session.scalar(query)
        return self._out.model_validate(res)
