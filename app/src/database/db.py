from os import getenv

from sqlalchemy import Engine
from sqlmodel import create_engine

from . import crud

DATABASE_URL: str = f"postgresql://{getenv("DATABASE_SERVER")}/pss-fleet-data?sslmode={getenv("DATABASE_SSL_MODE")}"
ENGINE: Engine = None


def initialize_db(engine: Engine, data_base_path: str = "examples"):
    crud.drop_tables(engine)
    crud.create_tables(engine)
    crud.create_dummy_data(engine, data_base_path)


def set_up_db_engine(database_url: str = None, echo: bool = True):
    if database_url:
        global DATABASE_URL
        DATABASE_URL = database_url
    global ENGINE
    ENGINE = create_engine(DATABASE_URL, echo=echo)


__all__ = [
    "ENGINE",
    initialize_db.__name__,
    set_up_db_engine.__name__,
]
