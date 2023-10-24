from fastapi import APIRouter

from family.services.health import HealthCheckService, HealthUOW

healthcheck = APIRouter(
    tags=["healthcheck"],
)


@healthcheck.get(
    "/healthcheck",
    summary="HealthCheck",
)
async def check():
    service = HealthCheckService(HealthUOW())
    return await service.check_connections()
