import json
from typing import AsyncGenerator

import pytest
import pytest_asyncio
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncTransaction, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.config import SETTINGS
from src.api.database import db
from src.api.database.models import CollectionDB


@pytest.fixture(scope="session", autouse=True)
async def initialize_database():
    db.set_up_db_engine(SETTINGS.async_database_connection_str, echo=True)
    db.initialize_db(True)
    await db.create_dummy_data(["tests/test_data/test_data.json"])
    await db.ENGINE.dispose()


@pytest.fixture(scope="function")
def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    async_engine = create_async_engine(SETTINGS.async_database_connection_str, echo=SETTINGS.database_engine_echo)
    return async_engine
    # await async_engine.dispose()


@pytest_asyncio.fixture(
    scope="function", autouse=True
)  # Set to "function", since "session" wouldn't allow to run all crud tests in quick succession.
async def session(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Provide a session that will automatically create and rollback transactions."""  # https://github.com/tiangolo/sqlmodel/discussions/940
    print("Set up database engine")

    connection: AsyncConnection = await async_engine.connect()
    transaction: AsyncTransaction = await connection.begin()

    async with AsyncSession(bind=connection) as async_session:
        nested = await connection.begin_nested()

        @sa.event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            nonlocal nested
            if not nested.is_active:
                nested = connection.sync_connection.begin_nested()

        print("yield session")
        yield async_session

        print("rollback transaction")
        await transaction.rollback()

    await connection.close()
    await async_engine.dispose()


@pytest.fixture(scope="session")
def test_data() -> dict:
    with open("tests/test_data/insert_test_data.json", "r") as fp:
        return json.load(fp)


@pytest.fixture(scope="function")
def new_collection(test_data) -> CollectionDB:
    collections = db.create_collections_from_dummy_data(test_data)
    return collections[0]
