from dataclasses import dataclass
from datetime import datetime, timezone
from os import getenv
from typing import Optional


@dataclass(frozen=True)
class Constants:
    """
    A collection of application-wide constants.
    """

    latest_schema_version: int = 9
    pss_start_date: datetime = datetime(2016, 1, 6, tzinfo=timezone.utc)


@dataclass(frozen=True)
class Settings:
    """
    A collection of application settings.
    """

    # Base
    project_name: str = "PSS Fleet Data API"
    version: str = "1.4.0"
    description: str = "An API server for Pixel Starships Fleet Data."
    contact = {
        "email": "theworstpss@gmail.com",
        "name": "The worst.",
        "url": "https://dolores2.xyz",
    }
    license = {
        "name": "MIT",
        "url": "https://github.com/Zukunftsmusik/pss-fleet-data-api/blob/main/LICENSE",
    }
    servers = [
        {
            "url": getenv("FLEET_DATA_API_URL_OVERRIDE", "https://fleetdata.dolores2.xyz"),
            "description": getenv("FLEET_DATA_API_URL_DESCRIPTION_OVERRIDE", "The original PSS Fleet Data API."),
            "variables": {},
        },
    ]

    # Database
    database_engine_echo: bool = getenv("DATABASE_ENGINE_ECHO", "false") == "true"
    async_database_connection_str: str = f"postgresql+asyncpg://{getenv("DATABASE_URL")}/{getenv("DATABASE_NAME", "pss-fleet-data")}"
    sync_database_connection_str: str = f"postgresql://{getenv("DATABASE_URL")}/{getenv("DATABASE_NAME", "pss-fleet-data")}"

    # Flags
    create_dummy_data_on_startup: bool = getenv("CREATE_DUMMY_DATA", "false") == "true"
    debug: bool = getenv("DEBUG_MODE", "false") == "true"
    in_github_actions: bool = getenv("GITHUB_ACTIONS", "false") == "true"  # True if in github actions
    reinitialize_database_on_startup: bool = getenv("REINITIALIZE_DATABASE", "false") == "true"

    # Access
    root_api_key: Optional[str] = getenv("ROOT_API_KEY", None)


SETTINGS = Settings()
CONSTANTS = Constants()
