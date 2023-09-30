from family.services.base import BaseService, BaseUOW


class HealthCheckService(BaseService):
    def __init__(self, uow: BaseUOW):
        ...

    async def check_me(self):
        return {"answer": "I am Root"}
