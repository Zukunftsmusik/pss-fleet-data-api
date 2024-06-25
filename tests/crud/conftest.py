from typing import Generator

import pytest
from sqlmodel import Session, create_engine

from src.database.db import set_up_db_engine, get_session

SQLITE_FILE_NAME = "test.sqlite"
DATABASE_URL = f"sqlite:///app/tests/{SQLITE_FILE_NAME}"


@pytest.fixture(scope="session")
def session() -> Generator[Session, None, None]:
    set_up_db_engine()
    with get_session() as session:
        yield session
