from fastapi import APIRouter

from family.services.health import HealthCheckService, HealthUOW

healthcheck = APIRouter()


@healthcheck.get(
    "/healthcheck",
    summary="HealthCheck",
    tags=["healthcheck"],
)
async def check():
    service = HealthCheckService(HealthUOW())
    return await service.check_connections()