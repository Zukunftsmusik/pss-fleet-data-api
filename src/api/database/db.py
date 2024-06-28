from os import getenv
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from . import crud

DATABASE_URL: str = f"postgresql+asyncpg://{getenv("DATABASE_SERVER")}/pss-fleet-data?sslmode={getenv("DATABASE_SSL_MODE")}"
ENGINE: AsyncEngine = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if not ENGINE:
        raise RuntimeError(f"ENGINE is `None`. The function {set_up_db_engine.__name__}() needs to get called first!")

    connection: AsyncConnection = await ENGINE.connect()
    async with AsyncSession(bind=connection) as async_session:
        try:
            yield async_session
        except Exception as e:
            await async_session.rollback()
            raise e
        finally:
            await async_session.close()

    await connection.close()


async def initialize_db(path_to_dummy_data: str = None):
    if not ENGINE:
        raise RuntimeError(f"ENGINE is `None`. The function {set_up_db_engine.__name__}() needs to get called first!")

    if not path_to_dummy_data:
        path_to_dummy_data = "examples/generated_dummy_data.json"

    await crud.drop_tables(ENGINE)
    await crud.create_tables(ENGINE)

    # connection: AsyncConnection = await ENGINE.connect()
    async with AsyncSession(ENGINE) as async_session:
        try:
            await crud.insert_dummy_data(async_session, [path_to_dummy_data])
        except Exception as e:
            await async_session.rollback()
            raise e
        finally:
            await async_session.close()

    # await connection.close()


def set_up_db_engine(database_url: str = None, echo: bool = True, is_sqlite: bool = False):
    if database_url:
        global DATABASE_URL
        DATABASE_URL = database_url
    connect_args = {}
    if is_sqlite:
        connect_args["check_same_thread"] = False

    global ENGINE
    ENGINE = create_async_engine(DATABASE_URL, echo=echo, future=True, connect_args=connect_args)


__all__ = [
    "ENGINE",
    initialize_db.__name__,
    set_up_db_engine.__name__,
]
