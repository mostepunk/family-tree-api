"""Базовый сервис."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from family.services.base import BaseUOW


class BaseService:
    def __init__(self, uow: "BaseUOW"):
        self.uow = uow
