"""Service getting information about Individual from family-tree."""

from loguru import logger as logging

from family.services.base import BaseService


class PersonService(BaseService):
    """Information about person in family-Tree."""

    async def info(self, person_id: str):
        async with self.uow:
            indi = await self.uow.persons.get_by_id(person_id)
            logging.info(f"Found Individual: {indi.id_}")
            return indi.dict()

    async def person_with_family(self, person_id: str):
        async with self.uow:
            (
                person,
                wifes,
                husbands,
                fathers,
                mothers,
            ) = await self.uow.persons.get_user_family(person_id)
            logging.info(f"WIFES: {len(wifes)}")
            logging.info(f"HUSBANDS: {len(husbands)}")
            logging.info(f"MOTHERS: {len(mothers)}")
            logging.info(f"FATHERS: {len(fathers)}")

            return {
                "person": person.dict(),
                "wifes": [wife.dict() for wife in wifes],
                "husbands": [husb.dict() for husb in husbands],
                "fathers": [father.dict() for father in fathers],
                "mothers": [mom.dict() for mom in mothers],
            }

    async def person_with_family_child(self, person_id: str):
        ...
