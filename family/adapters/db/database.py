import asyncio
from typing import Callable

from loguru import logger as logging
from sqlalchemy import orm, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from family.settings import DatabaseSettings, db_settings

engine = create_async_engine(
    db_settings.dsn,
    pool_pre_ping=True,
    pool_use_lifo=True,
    pool_size=20,
    echo=False,
    # echo=True,
    max_overflow=5,
)
async_session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)

NUMBER_OF_ATTEMPTS = 3
TIME_SLEEP = 5


def create_start_app_handler() -> Callable:
    """create_start_app_handler.

    Returns:
        Callable:
    """

    async def check_database() -> None:
        """check database connection."""
        attempt = 0
        while True:
            try:
                async with engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
                    logging.debug("DB connected")
                    break
            except Exception as err:  # noqa:BLE001
                logging.error(f"ERROR: {err}")
                if attempt < NUMBER_OF_ATTEMPTS:
                    logging.error(f"try connect to db...{attempt}")
                    attempt += 1
                    await asyncio.sleep(TIME_SLEEP)
                else:
                    logging.critical("Can`t connect to DB")
                    raise err  # noqa:TRY201 Use `raise` without specifying exception name

    return check_database


async def get_session() -> AsyncSession:
    """get session.

    Returns:
        AsyncSession:
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


class Database:
    """Database Singleton for UOW Container."""

    def __init__(self, db_settings: DatabaseSettings) -> None:
        self._engine = create_async_engine(
            db_settings.dsn,
            pool_pre_ping=True,
            pool_use_lifo=True,
            pool_size=20,
            echo=db_settings.echo,
            echo_pool=db_settings.echo_pool,
            max_overflow=5,
        )
        self._session_factory = orm.scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                class_=AsyncSession,
                bind=self._engine,
                expire_on_commit=False,
            ),
        )

    def session(self):
        """session."""
        return self._session_factory()
