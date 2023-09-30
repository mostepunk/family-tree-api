"""Router v1 for Receipt-service."""

from fastapi import APIRouter

from family.api.v1.root import root_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(root_router)
