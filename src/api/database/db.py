import json
from typing import AsyncGenerator, Union

from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from alembic import command
from alembic.config import Config as AlembicConfig

from .. import utils
from ..config import SETTINGS
from . import crud
from .models import AllianceDB, CollectionDB, UserDB


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

        collected_data["metadata"]["data_version"] = collected_data["metadata"].pop("schema_version", 3)
        collection = CollectionDB(**(collected_data["metadata"]), alliances=alliances, users=users)
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

    await insert_dummy_collection(collections)


async def insert_dummy_collection(collections: list[CollectionDB]):
    """Attempts to insert the provided `collections` into the database. If inserting a Collection fails, the transaction will be rolled back and the error will be printed to stdout.

    Args:
        collections (list[CollectionDB]): The Collections to be inserted.
    """
    for collection in collections:
        async for session in get_session():
            try:
                collection = await crud.save_collection(session, collection, True, True)
            except DBAPIError as exc:
                print(f"Could not insert dummy Collection:\n{exc}")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Creates and returns an `AsyncSession` from the `ENGINE` in this module. If an error occurs during a session, the changes will be rolled back and the exception will be raised again.

    Raises:
        RuntimeError: Raised, if `ENGINE` in this module hasn't been initialized, yet.
        DBAPIError: Raised, if an error occurs during a transaction.

    Returns:
        AsyncGenerator[AsyncSession, None]: _description_

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


async def initialize_db(drop_tables: bool = False, paths_to_dummy_data: list[str] = None):
    """Initializes the database. Optionally drops all tables before creating them. Optionally dummy data will be read from disk and inserted.

    Args:
        drop_tables (bool, optional): Determines, if all tables should be dropped before being recreated. Defaults to False.
        paths_to_dummy_data (list[str], optional): The paths to files with verbose Collection data. Defaults to None.

    Raises:
        RuntimeError: Raised, if `ENGINE` in this module hasn't been initialized, yet.
    """
    if not ENGINE:
        raise RuntimeError(f"ENGINE is `None`. The function {set_up_db_engine.__name__}() needs to get called first!")

    if drop_tables:
        await crud.drop_tables(ENGINE)

    await run_migrations()

    await crud.create_tables(ENGINE)

    if paths_to_dummy_data:
        await create_dummy_data(paths_to_dummy_data)


async def run_migrations():
    if not ENGINE:
        raise RuntimeError(f"ENGINE is `None`. The function {set_up_db_engine.__name__}() needs to get called first!")

    async with ENGINE.begin() as connection:
        await connection.run_sync(run_upgrade, AlembicConfig("src/alembic.ini"))


def run_upgrade(connection: AsyncConnection, alembic_config: AlembicConfig):
    """Applies all database migrations until the database schema is fully upgraded.

    Args:
        connection (AsyncConnection): A connection to the database to be migrated.
        alembic_config (AlembicConfig): The `alembic` configuration.
    """
    alembic_config.attributes["sqlalchemy.url"] = SETTINGS.database_connection_str
    alembic_config.attributes["connection"] = connection
    command.upgrade(alembic_config, "head")


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
    ENGINE = create_async_engine(database_url, echo=echo, future=True, connect_args=connect_args)


__all__ = [
    "ENGINE",
    get_session.__name__,
    initialize_db.__name__,
    set_up_db_engine.__name__,
]
