from family.api.v1.router import v1_router
from family.application import create_app
from family.core.midlewares import LoggingMiddleware
from family.settings import app_settings

app = create_app()
app.include_router(v1_router, prefix=app_settings.api_prefix)
app.middleware("http")(LoggingMiddleware())
