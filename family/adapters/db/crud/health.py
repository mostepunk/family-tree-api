from typing import NoReturn

from loguru import logger as logging
from sqlalchemy import text

from family.adapters.db.crud.base import BaseCRUD


class HealthCRUD(BaseCRUD):
    """HealthCRUD."""

    async def check_database(self) -> NoReturn:
        """check database connection."""
        res = await self.session.execute(text("SELECT VERSION()"))
        results = res.fetchone()
        if results:
            logging.debug("[HELATH]: Database OK")
