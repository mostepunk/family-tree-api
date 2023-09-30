from fastapi import HTTPException

from family.services.base import BaseService


class HealthCheckService(BaseService):
    """Check health of connections for service."""

    async def check_connections(self) -> str:
        """check_me.

        Raises:
            HTTPException: 409 if something goes wrong

        Returns:
            str: "OK"
        """
        async with self.uow:
            try:
                await self.uow.health.check_database()
            except BaseException as err:
                raise HTTPException(status_code=409, detail=str(err))
            else:
                return "OK"
