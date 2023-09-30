import uvicorn

from family.api.v1.router import v1_router
from family.application import create_app
from family.core.midlewares import LoggingMiddleware
from family.settings import app_settings

app = create_app(app_settings.api_kwargs)
app.include_router(v1_router, prefix=app_settings.api_prefix)
app.middleware("http")(LoggingMiddleware())


if __name__ == "__main__":
    uvicorn.run("__main__:app", port=80, reload=True)
