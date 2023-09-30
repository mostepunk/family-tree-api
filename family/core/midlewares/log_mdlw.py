"""Мидлварь для логгирования запросов и ответов."""

import dataclasses
import http
import math
import time
from typing import ClassVar

import stackprinter
from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import Receive

from family.adapters.schemas.logging_schema import MWValidator
from family.settings import app_settings

EMPTY_VALUE = ""
NULL = "null"


@dataclasses.dataclass
class ReceiveProxy:
    """Proxy to starlette.types.Receive.__call__ with caching first receive call.

    https://github.com/tiangolo/fastapi/issues/394#issuecomment-994665859
    """

    receive: Receive
    cached_body: bytes
    _is_first_call: ClassVar[bool] = True

    async def __call__(self):
        """First call will be for getting request body => returns cached result.

        Returns:
            словарь.
        """
        if self._is_first_call:
            self._is_first_call = False
            return {
                "type": "http.request",
                "body": self.cached_body,
                "more_body": False,
            }

        return await self.receive()


class LoggingMiddleware:
    """Middleware для обработки запросов и ответов с целью журналирования.

    Основная проблема с этой мидлварью в том, что при получении тела запроса
        body = await request.body()
    Оно затирается и перестает работать.
    Пришлось искать решение на стороне и делать вспомогательный объект ReceiveProxy.
    """

    @staticmethod
    async def get_protocol(request: Request) -> str:
        """Получить протокол.

        Args:
            request: ...

        Returns:
            str: ...
        """
        protocol = str(request.scope.get("type", ""))
        http_version = str(request.scope.get("http_version", ""))
        if protocol.lower() == "http" and http_version:
            return f"{protocol.upper()}/{http_version}"
        return EMPTY_VALUE

    async def get_request_body(self, request: Request) -> bytes:
        """Получить тело запроса.

        Args:
            request: ...

        Returns:
            bytes: ...
        """
        body = await request.body()

        request._receive = ReceiveProxy(receive=request.receive, cached_body=body)
        return body

    async def __call__(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
        *args,
        **kwargs,
    ):
        """Вызов мидлвари.

        Args:
            request: ...
            call_next: ...
            args: ...
            kwargs: ...

        Returns:
            reponse: ...
        """
        start_time = time.time()
        exception_object = NULL
        request_body = await self.get_request_body(request)

        # Response Side
        try:
            response = await call_next(request)
        except Exception as ex:
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = stackprinter.format(
                ex,
                suppressed_paths=[
                    r"/usr/local/lib/python3.10/site-packages.*",
                ],
                add_summary=False,
            )
            delimiter = f"\t{'='*30}\n"
            overview = f"{delimiter}\tException {ex}:\n{delimiter}"
            logger.error(f"\n{exception_object}\n{overview}")
        else:
            response_body = b""

            async for chunk in response.body_iterator:
                response_body += chunk

            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        if request.url.path in app_settings.pass_routes:
            return response

        duration: int = math.ceil((time.time() - start_time) * 1000)

        valid = MWValidator(
            response_body=response_body, request_body=request_body, url=str(request.url)
        )
        message = (
            f'{"Ошибка" if exception_object != NULL else "Ответ"} '
            f"с кодом {response.status_code} "
            f'на запрос {request.method} "{valid.url}" '
            f"за {duration} мс "
            f"тело запроса: {valid.request_body} "
            f"тело ответа: {valid.response_body} "
        )
        logger.bind(exceptions=exception_object).info(
            message,
        )
        return response
