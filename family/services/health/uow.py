from family.adapters.db.crud.health import HealthCRUD
from family.services.base import BaseUOW


class HealthUOW(BaseUOW):
    async def __aenter__(self):
        self.session = self.session_factory()
        self.health = HealthCRUD(self.session)
