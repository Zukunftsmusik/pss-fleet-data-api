from typing import Generator

import pytest
import sqlalchemy as sa
from sqlmodel import Session

from src.api.database import db

SQLITE_FILE_NAME = "test.sqlite"
DATABASE_URL = f"sqlite:///app/tests/{SQLITE_FILE_NAME}"


@pytest.fixture(scope="session")
def session() -> Generator[Session, None, None]:
    """Provide a session that will automatically create and rollback transactions."""  # https://github.com/tiangolo/sqlmodel/discussions/940
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

    yield session

    session.close()
    transaction.rollback()
    connection.close()
