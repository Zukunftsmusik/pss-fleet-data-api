from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import exception_handlers
from .config import SETTINGS
from .database import db
from .models.exceptions import (
    ConflictError,
    MethodNotAllowedError,
    MissingAccessError,
    NotAuthenticatedError,
    NotFoundError,
    ParameterValidationError,
    ServerError,
)
from .routers import alliances, collections, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_app(
        app,
        SETTINGS.database_connection_str,
        SETTINGS.debug,
        SETTINGS.reinitialize_database_on_startup,
        SETTINGS.create_dummy_data_on_startup,
    )
    yield


app = FastAPI(
    version=SETTINGS.version,
    title=SETTINGS.project_name,
    description=SETTINGS.description,
    contact={"email": "theworstpss@gmail.com", "name": "The worst.", "url": "https://dolores2.xyz"},
    license={"name": "MIT", "url": "https://github.com/Zukunftsmusik/pss-fleet-data-api/blob/main/LICENSE"},
    # servers=[{"url": "https://fleetdata.dolores2.xyz", "description": "The PSS Fleet Data API.", "variables": {}}],
    lifespan=lifespan,
)
app.include_router(alliances.router)
app.include_router(collections.router)
app.include_router(users.router)

app.add_exception_handler(StarletteHTTPException, exception_handlers.handle_http_exception)
app.add_exception_handler(NotAuthenticatedError, exception_handlers.handle_not_authenticated)
app.add_exception_handler(MissingAccessError, exception_handlers.handle_missing_access)
app.add_exception_handler(NotFoundError, exception_handlers.handle_not_found)
app.add_exception_handler(MethodNotAllowedError, exception_handlers.handle_method_not_allowed)
app.add_exception_handler(ConflictError, exception_handlers.handle_conflict)
app.add_exception_handler(ParameterValidationError, exception_handlers.handle_parameter_validation)
app.add_exception_handler(RequestValidationError, exception_handlers.handle_request_validation)
app.add_exception_handler(ServerError, exception_handlers.handle_server)


async def initialize_app(app: FastAPI, database_connection_string: str, echo: bool, reinitialize_database: bool, create_dummy_data: bool):
    """Initialize the API.

    Args:
        app (FastAPI): The FastAPI app.
        database_connection_string (str): The database connection string to be used.
        echo (bool): Determines, if SQL statements should be printed to stdout.
        reinitialize_database (bool): Determines, if the database tables should be dropped on app startup.
        create_dummy_data (bool): Determines, if dummy data should be attempted to be inserted on app startup.
    """
    db.set_up_db_engine(database_connection_string, echo=echo)

    paths_to_dummy_data = None
    if create_dummy_data:
        paths_to_dummy_data = ["examples/generated_dummy_data.json"]

    await db.initialize_db(reinitialize_database, paths_to_dummy_data)
