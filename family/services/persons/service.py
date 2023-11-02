"""Service getting information about Individual from family-tree."""

from loguru import logger as logging

from family.services.base import BaseService


class PersonService(BaseService):
    """Information about person in family-Tree."""

    async def info(self, person_id: str):
        async with self.uow:
            res = await self.uow.persons.get_by_id(person_id)
            logging.info(f"Found in DB: {res}")
            return res
