import io
import json
from typing import AsyncGenerator, Union

import alembic.command
import sqlalchemy_utils
from alembic.config import Config as AlembicConfig
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import utils
from ..config import SETTINGS
from . import crud

# v Required for SQLModel.metadata.drop_all()
from .models import AllianceBaseDB, AllianceDB, CollectionBaseDB, CollectionDB, UserBaseDB, UserDB  # noqa: F401


ENGINE: AsyncEngine = None


def create_collections_from_dummy_data(data: Union[dict, list[dict]]) -> list[CollectionDB]:
    """Takes verbose Collection dummy data from a file and converts it to a list of `CollectionDB` objects.

    Args:
        data (Union[dict, list[dict]]): Either a verbose Collection or a list of verbose Collections read from a file.

    Returns:
        list[CollectionDB]: The converted data.
    """
    collections = []

    if not isinstance(data, list):
        data = [data]

    for collected_data in data:
        alliances = [AllianceDB(**alliance) for alliance in collected_data["fleets"]]
        users = [UserDB(**user) for user in collected_data["users"]]
        for user in users:
            user.alliance_join_date = utils.parse_datetime(user.alliance_join_date).replace(tzinfo=None) if user.alliance_join_date else None
            user.last_login_date = utils.parse_datetime(user.last_login_date).replace(tzinfo=None) if user.last_login_date else None
            user.last_heartbeat_date = utils.parse_datetime(user.last_heartbeat_date).replace(tzinfo=None) if user.last_heartbeat_date else None

        collected_data["meta"]["data_version"] = collected_data["meta"].pop("schema_version", 3)
        collection = CollectionDB(**(collected_data["meta"]), alliances=alliances, users=users)
        collection.collected_at = utils.parse_datetime(collection.collected_at).replace(tzinfo=None) if collection.collected_at else None

        for i, alliance in enumerate(alliances):
            if not alliance.trophy:
                alliance.trophy = sum(user.trophy for user in users if user.alliance_id == alliance.alliance_id)

            if collection.tournament_running and alliance.division_design_id is None:
                if i < 8:
                    alliance.division_design_id = 1
                elif i < 20:
                    alliance.division_design_id = 2
                elif i < 50:
                    alliance.division_design_id = 3
                else:
                    alliance.division_design_id = 4

        collections.append(collection)

    return collections


async def create_dummy_data(paths_to_dummy_data: list[str]):
    """Reads dummy data from the provided file paths and attempts to insert it into the database.

    Args:
        paths_to_dummy_data (list[str]): A collection of paths to files containing dummy data.
    """
    collections = []
    for file_path in paths_to_dummy_data:
        with open(file_path, "r") as fp:
            data = json.load(fp)

        collections.extend(create_collections_from_dummy_data(data))

    await insert_dummy_collections(collections)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Creates and returns an `AsyncSession` from the `ENGINE` in this module. If an error occurs during a session, the changes will be rolled back and the exception will be raised again.

    Raises:
        RuntimeError: Raised, if `ENGINE` in this module hasn't been initialized, yet.
        DBAPIError: Raised, if an error occurs during a transaction.

    Returns:
        AsyncGenerator[AsyncSession, None]: Returns a single `AsyncSession` when iterating.

    Yields:
        AsyncSession: The created `AsyncSession` object.
    """
    if not ENGINE:
        raise RuntimeError(f"ENGINE is `None`. The function {set_up_db_engine.__name__}() needs to get called first!")

    connection: AsyncConnection = await ENGINE.connect()
    try:
        async with AsyncSession(bind=connection) as async_session:
            try:
                yield async_session
            except DBAPIError as session_exception:
                await async_session.rollback()
                raise session_exception
            finally:
                await async_session.close()
    except DBAPIError as connection_exception:
        print(connection_exception)
        raise connection_exception
    finally:
        await connection.close()


async def insert_dummy_collections(collections: list[CollectionDB]):
    """Attempts to insert the provided `collections` into the database. If inserting a Collection fails, the transaction will be rolled back and the error will be printed to stdout.

    Args:
        collections (list[CollectionDB]): The Collections to be inserted.
    """
    async for session in get_session():
        for collection in collections:
            try:
                collection = await crud.save_collection(session, collection, True, True)
            except DBAPIError as exc:
                print(f"Could not insert dummy Collection:\n{exc}")


def initialize_db(reinitialize: bool = False):
    """Initializes the database. Optionally drops all tables before creating them. Optionally dummy data will be read from disk and inserted.

    Args:
        drop_tables (bool, optional): Determines, if all tables should be dropped before being recreated. Defaults to False.
        paths_to_dummy_data (list[str], optional): The paths to files with verbose Collection data. Defaults to None.

    Raises:
        RuntimeError: Raised, if `ENGINE` in this module hasn't been initialized, yet.
    """
    sync_connection_string = SETTINGS.sync_database_connection_str

    if not sqlalchemy_utils.database_exists(sync_connection_string):
        sqlalchemy_utils.create_database(sync_connection_string)

    if reinitialize:
        __drop_tables(sync_connection_string)

    if not __alembic_current_is_head(sync_connection_string):
        alembic_config = AlembicConfig("alembic.ini")
        alembic_config.attributes["sqlalchemy.url"] = sync_connection_string
        alembic.command.upgrade(alembic_config, "head", tag="from_app")


def set_up_db_engine(database_url: str, echo: bool = None):
    """Initializes the database engine `ENGINE`.

    Args:
        database_url (str): The full url to the database, including: dialect, username, password, server url or IP address & port.
        echo (bool, optional): Determines, if the issued SQL statements should be written to stdout. Defaults to None.
    """
    if echo is None:
        echo = SETTINGS.database_engine_echo

    connect_args = {}

    global ENGINE
    ENGINE = create_async_engine(database_url, echo=echo, future=True, connect_args=connect_args, pool_pre_ping=True)
    # pool_pre_ping fixes Issue #20 according to https://github.com/MagicStack/asyncpg/issues/309#issuecomment-1987144710


def __alembic_current_is_head(sync_connection_string: str):
    output_buffer = io.StringIO()

    alembic_config = AlembicConfig("alembic.ini", stdout=output_buffer)
    alembic_config.attributes["sqlalchemy.url"] = sync_connection_string

    alembic.command.current(alembic_config)
    current = output_buffer.getvalue()

    return "(head)" in current


def __drop_tables(connection_str: str):
    engine = create_engine(connection_str, poolclass=NullPool)
    SQLModel.metadata.drop_all(engine)
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS alembic_version;"))
    engine.dispose()


__all__ = [
    "ENGINE",
    create_collections_from_dummy_data.__name__,
    create_dummy_data.__name__,
    get_session.__name__,
    initialize_db.__name__,
    insert_dummy_collections.__name__,
    set_up_db_engine.__name__,
]
