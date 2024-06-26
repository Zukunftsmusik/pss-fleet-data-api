import json
from typing import Generator

import pytest
import sqlalchemy as sa
from sqlmodel import Session

from src.api.database import db
from src.api.database.models import AllianceDB, CollectionDB, UserDB

SQLITE_FILE_NAME = "test.sqlite"
DATABASE_URL = f"sqlite:///app/tests/{SQLITE_FILE_NAME}"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DummyData(metaclass=Singleton):
    data: dict = {}

    def __init__(self):
        if not self.data:
            with open("examples/dummy_data.json", "r") as fp:
                self.data = json.load(fp)

    def get_dummy_collection(self) -> CollectionDB:
        data = self.data

        alliances = [AllianceDB(**alliance) for alliance in data["fleets"]]
        users = [UserDB(**user) for user in data["users"]]

        collection = CollectionDB(**(data["metadata"]), alliances=alliances, users=users)

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

        return collection


@pytest.fixture(scope="function", autouse=True)  # Set to "function", since "session" wouldn't allow to run all crud tests in quick succession.
def session() -> Generator[Session, None, None]:
    """Provide a session that will automatically create and rollback transactions."""  # https://github.com/tiangolo/sqlmodel/discussions/940
    print("Set up database engine")
    db.set_up_db_engine()

    connection = db.ENGINE.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    nested = connection.begin_nested()

    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    print("yield session")
    yield session

    session.close()
    print("rollback transaction")
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def new_collection() -> CollectionDB:
    dummy_data = DummyData()
    return dummy_data.get_dummy_collection()
