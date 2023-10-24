"""Базовый UnitOfWork."""

from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    def __await__(self):
        return self.__aenter__().__await__()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class BaseUOW(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

    async def __aexit__(self, *args):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def close(self):
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()
