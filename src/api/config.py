from os import getenv
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings():
   # Base
   initialize_database_on_startup: bool = False
   in_github_actions: bool = bool(getenv("IN_GITHUB_ACTIONS", False))
   debug: bool = bool(getenv("DEBUG_MODE", False))
   testing: bool = bool(getenv("TEST_MODE", False))
   project_name: str = "PSS Fleet Data API"
   version: str = "1.0"
   description: str = "An API server for Pixel Starships Fleet Data."

   # Database
   database_engine_echo: bool = False
   database_connection_str: str = f"postgresql+asyncpg://{getenv("DATABASE_USER")}:{getenv("DATABASE_PASSWORD")}@{getenv("DATABASE_SERVER")}/pss-fleet-data?sslmode={getenv("DATABASE_SSL_MODE")}"
   database_test_connection_str: str = f"postgresql+asyncpg://{getenv("DATABASE_USER")}:{getenv("DATABASE_PASSWORD")}@{getenv("DATABASE_SERVER")}/pss-fleet-data-test"
   x = 4


SETTINGS = Settings()
