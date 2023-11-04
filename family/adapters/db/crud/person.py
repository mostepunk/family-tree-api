from sqlalchemy import select
from sqlalchemy.orm import selectinload

from family.adapters.db.crud.base import BaseCRUD
from family.adapters.db.models import FamilyModel, PersonModel
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
        return res
        # return res.individual

    async def get_user_family(self, person_id: str):
        query = (
            select(PersonModel)
            .where(PersonModel.i_id == person_id)
            .options(
                selectinload(PersonModel.families).joinedload(
                    FamilyModel.husband,
                ),
                selectinload(PersonModel.families).joinedload(
                    FamilyModel.wife,
                ),
            )
        )
        return await self.session.scalar(query)
