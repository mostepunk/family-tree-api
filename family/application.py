from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from family.adapters.db.database import create_start_app_handler
from family.api.errors import http_error_handler
from family.settings import app_settings
from family.utils.container import Container


def create_app(fastapi_settings: dict) -> FastAPI:
    container = Container()
    application = FastAPI(**fastapi_settings)
    application.container = container

    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(),
    )

    application.add_exception_handler(HTTPException, http_error_handler)

    return application
