"""Настройки логгирования."""

import logging
import sys
from types import FrameType
from typing import cast

from loguru import logger

from family.settings import app_settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """Get corresponding Loguru level if it exists.

        Args:
            record: объект LogRecord
        """
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        """Фильтр запросов, которые не надо логгировать.

        Args:
            record: объект LogRecord

        Returns:
            bool: True если соответствует условию
        """
        request_method = record.args[1]
        # complete query string (so parameter and other value included)
        query_string = record.args[2]

        # return request_method == "GET" and query_string not in app_settings.pass_routes
        return query_string not in app_settings.pass_routes


LOGGING_LEVEL = app_settings.log_level
LOGGERS = (
    "uvicorn",
    "uvicorn.asgi",
    "uvicorn.error",
    "fastapi",
    "uvicorn.access",
)

logging.getLogger().handlers = [InterceptHandler()]

for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stdout, "level": LOGGING_LEVEL}])

# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
