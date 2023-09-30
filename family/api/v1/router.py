"""Router v1 for Receipt-service."""

from fastapi import APIRouter

from family.api.v1.healthcheck import healthcheck

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(healthcheck)
