import json
from os import getenv
from typing import AsyncGenerator

import pytest
import pytest_asyncio
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncTransaction, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database import crud, db
from src.api.database.models import CollectionDB
from src.api.config import SETTINGS

if SETTINGS.in_github_actions:
    pytest.skip("These tests require a postgres DB", allow_module_level=True)


@pytest.fixture(scope="session", autouse=True)
async def initialize_database():
    db.set_up_db_engine(SETTINGS.database_test_connection_str, echo=SETTINGS.database_engine_echo)
    await db.initialize_db("src/tests/02_database/test_data.json")
    await db.ENGINE.dispose()


@pytest.fixture(scope="function")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    async_engine = create_async_engine(SETTINGS.database_test_connection_str, echo=SETTINGS.database_engine_echo)
    yield async_engine
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function", autouse=True)  # Set to "function", since "session" wouldn't allow to run all crud tests in quick succession.
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
    # await async_session.close()
    await connection.close()


@pytest.fixture(scope="session")
def test_data() -> dict:
    with open("src/tests/02_database/insert_test_data.json", "r") as fp:
        return json.load(fp)


@pytest.fixture(scope="function")
def new_collection(test_data) -> CollectionDB:
    collections = crud.create_collections_from_dummy_data(test_data)
    return collections[0]
