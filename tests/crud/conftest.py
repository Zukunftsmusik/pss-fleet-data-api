from typing import Generator

import pytest
from sqlmodel import Session, create_engine

from src.api.database import db

SQLITE_FILE_NAME = "test.sqlite"
DATABASE_URL = f"sqlite:///app/tests/{SQLITE_FILE_NAME}"


@pytest.fixture(scope="session")
def session() -> Generator[Session, None, None]:
    db.set_up_db_engine()
    with Session(db.ENGINE) as session:
        yield session
