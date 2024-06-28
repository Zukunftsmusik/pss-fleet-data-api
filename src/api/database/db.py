from os import getenv
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from . import crud

DATABASE_URL: str = f"postgresql+asyncpg://{getenv("DATABASE_SERVER")}/pss-fleet-data?sslmode={getenv("DATABASE_SSL_MODE")}"
ENGINE: AsyncEngine = None

SESSION_LOCAL = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if not ENGINE:
        raise Exception(f"ENGINE is `None`. The function {set_up_db_engine.__name__}() needs to get called first!")

    async_session = sessionmaker(ENGINE, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


async def get_session():
    async with SESSION_LOCAL() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def initialize_db():
    if not ENGINE:
        raise Exception(f"ENGINE is `None`. The function {set_up_db_engine.__name__}() needs to get called first!")

    await crud.drop_tables(ENGINE)
    await crud.create_tables(ENGINE)
    await crud.insert_dummy_data(ENGINE, ["examples/generated_dummy_data.json"])


def set_up_db_engine(database_url: str = None, echo: bool = True, is_sqlite: bool = False):
    if database_url:
        global DATABASE_URL
        DATABASE_URL = database_url
    connect_args = {}
    if is_sqlite:
        connect_args["check_same_thread"] = False

    global ENGINE
    ENGINE = create_async_engine(DATABASE_URL, echo=echo, future=True, connect_args=connect_args)

    global SESSION_LOCAL
    SESSION_LOCAL = sessionmaker(
        bind=ENGINE,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )


__all__ = [
    "ENGINE",
    initialize_db.__name__,
    set_up_db_engine.__name__,
]
