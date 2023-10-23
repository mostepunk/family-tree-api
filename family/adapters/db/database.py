import asyncio
from typing import Callable

from loguru import logger as logging
from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from family.adapters.db.models import AccountModel, RoleModel
from family.settings import admin_settings, db_settings

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


async def create_superadmin(session):
    query = select(RoleModel.uuid).where(RoleModel.name == "ROOT")
    role_uuid = await session.scalar(query)

    credentials = admin_settings.credentials
    credentials["role_uuid"] = role_uuid

    query = pg_insert(AccountModel).values(credentials).returning(AccountModel)
    admin = await session.scalar(query.on_conflict_do_nothing())
    await session.commit()

    if admin:
        logging.debug(f"Created SuperUser: {admin}")


def create_start_app_handler() -> Callable:
    async def check_database() -> None:
        attempt = 0
        while True:
            try:
                async with engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
                    logging.debug("DB connected")
                    await create_superadmin(conn)
                    break
            except Exception as err:
                logging.error(f"ERROR: {err}")
                if attempt < NUMBER_OF_ATTEMPTS:
                    logging.error(f"try connect to db...{attempt}")
                    attempt += 1
                    await asyncio.sleep(TIME_SLEEP)
                else:
                    logging.critical("Can`t connect to DB")
                    raise err

    return check_database


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            # это надо при подключении через PGBouncer
            # await session.rollback()
            await session.close()
