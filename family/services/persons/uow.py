from family.adapters.db.crud import PersonCRUD
from family.services.base import BaseUOW


class PersonUOW(BaseUOW):
    async def __aenter__(self):
        self.session = self.session_factory()
        self.persons = PersonCRUD(self.session)
