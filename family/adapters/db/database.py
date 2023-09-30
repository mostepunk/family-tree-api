import asyncio
from typing import Callable

from loguru import logger as logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from family.settings import db_settings

engine = create_async_engine(
    db_settings.dsn,
    pool_pre_ping=True,
    pool_use_lifo=True,
    pool_size=20,
    echo=False,
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
    async def check_database() -> None:
        attempt = 0
        while True:
            try:
                async with engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
                    logging.info("DB connected")
                    break
            except Exception as err:
                if attempt < NUMBER_OF_ATTEMPTS:
                    logging.error(f"try connect to db...{attempt}")
                    attempt += 1
                    await asyncio.sleep(TIME_SLEEP)
                else:
                    logging.critical("Can`t connect to DB")
                    raise err

    return check_database
