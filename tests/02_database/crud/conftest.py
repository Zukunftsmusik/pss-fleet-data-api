import json
from os import getenv
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    AsyncConnection,
    AsyncTransaction,
    AsyncEngine
)
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.api.database import db
from src.api.database.models import AllianceDB, CollectionDB, UserDB

from src.api import utils

if getenv("IN_GITHUB_ACTIONS"):
    pytest.skip("These tests require a postgres DB", allow_module_level=True)


@pytest.fixture(scope="function")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    async_engine = create_async_engine(f"postgresql+asyncpg://{getenv("DATABASE_SERVER")}/pss-fleet-data", echo=True)
    yield async_engine
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function", autouse=True)  # Set to "function", since "session" wouldn't allow to run all crud tests in quick succession.
async def session(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Provide a session that will automatically create and rollback transactions."""  # https://github.com/tiangolo/sqlmodel/discussions/940
    print("Set up database engine")

    connection: AsyncConnection = await async_engine.connect()
    transaction: AsyncTransaction = await connection.begin()
    # async_session = AsyncSession(bind=connection)
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
def dummy_data() -> dict:
    with open("examples/dummy_data.json", "r") as fp:
        return json.load(fp)
    

from src.api.models.converters import ToDB


@pytest.fixture(scope="function")
def new_collection(dummy_data) -> CollectionDB:
    alliances = [AllianceDB(**alliance) for alliance in dummy_data["fleets"]]
    users = [UserDB(**user) for user in dummy_data["users"]]
    for user in users:
        user.alliance_join_date = utils.parse_datetime(user.alliance_join_date).replace(tzinfo=None) if user.alliance_join_date else None
        user.last_login_date = utils.parse_datetime(user.last_login_date).replace(tzinfo=None) if user.last_login_date else None
        user.last_heartbeat_date = utils.parse_datetime(user.last_heartbeat_date).replace(tzinfo=None) if user.last_heartbeat_date else None

    collection = CollectionDB(**(dummy_data["metadata"]), alliances=alliances, users=users)
    collection.collected_at = utils.parse_datetime(collection.collected_at).replace(tzinfo=None) if collection.collected_at else None
    return collection
