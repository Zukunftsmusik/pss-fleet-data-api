from os import getenv
from typing import Generator

from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from . import crud

DATABASE_URL: str = f"postgresql://{getenv("DATABASE_SERVER")}/pss-fleet-data?sslmode={getenv("DATABASE_SSL_MODE")}"
ENGINE: Engine = None


def get_session() -> Generator[Session, None, None]:
    if not ENGINE:
        raise Exception(f"ENGINE is `None`. The function {set_up_db_engine.__name__}() needs to get called first!")

    with Session(ENGINE) as session:
        yield session


def initialize_db():
    if not ENGINE:
        raise Exception(f"ENGINE is `None`. The function {set_up_db_engine.__name__}() needs to get called first!")

    crud.drop_tables(ENGINE)
    crud.create_tables(ENGINE)
    crud.insert_dummy_data(ENGINE, ["examples/generated_dummy_data.json"])


def set_up_db_engine(database_url: str = None, echo: bool = True, is_sqlite: bool = False):
    if database_url:
        global DATABASE_URL
        DATABASE_URL = database_url
    global ENGINE
    connect_args = {}
    if is_sqlite:
        connect_args["check_same_thread"] = False
    ENGINE = create_engine(DATABASE_URL, echo=echo, connect_args=connect_args)


__all__ = [
    "ENGINE",
    initialize_db.__name__,
    set_up_db_engine.__name__,
]
