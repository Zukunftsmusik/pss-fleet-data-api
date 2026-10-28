from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import exception_handlers
from .config import CONSTANTS, SETTINGS
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
from .response_cache import RESPONSE_CACHE, ResponseCacheMiddleware
from .routers import alliances, collections, root, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages setup and teardown of the Fleet Data API.

    Args:
        app (FastAPI): The FastAPI app.
    """
    print(f"Initializing {app.title}")
    print(f"Version: {app.version}")
    print(f"Latest schema version: {CONSTANTS.latest_schema_version}")
    print(f"Debug mode: {SETTINGS.debug}")
    print(f"Reinitialize database: {SETTINGS.reinitialize_database_on_startup}")
    print(f"Insert dummy data: {SETTINGS.create_dummy_data_on_startup}")
    print(f"In github action: {SETTINGS.in_github_actions}")

    await initialize_app(
        app,
        SETTINGS.async_database_connection_str,
        SETTINGS.debug,
        SETTINGS.reinitialize_database_on_startup,
        SETTINGS.create_dummy_data_on_startup,
    )

    yield


app = FastAPI(
    version=SETTINGS.version,
    title=SETTINGS.project_name,
    description=SETTINGS.description,
    contact=SETTINGS.contact,
    license=SETTINGS.license,
    servers=SETTINGS.servers,
    lifespan=lifespan,
    swagger_ui_parameters={"syntaxHighlight": False},  # Increases performance on large responses
    strict_content_type=False,
)


app.include_router(alliances.router)
app.include_router(collections.router)
app.include_router(users.router)
app.include_router(root.router)


app.add_middleware(GZipMiddleware, minimum_size=1)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


app.add_exception_handler(StarletteHTTPException, exception_handlers.handle_http_exception)
app.add_exception_handler(NotAuthenticatedError, exception_handlers.handle_not_authenticated)
app.add_exception_handler(MissingAccessError, exception_handlers.handle_missing_access)
app.add_exception_handler(NotFoundError, exception_handlers.handle_not_found)
app.add_exception_handler(MethodNotAllowedError, exception_handlers.handle_method_not_allowed)
app.add_exception_handler(ConflictError, exception_handlers.handle_conflict)
app.add_exception_handler(ParameterValidationError, exception_handlers.handle_parameter_validation)
app.add_exception_handler(RequestValidationError, exception_handlers.handle_request_validation)
app.add_exception_handler(ServerError, exception_handlers.handle_server)

if not SETTINGS.disable_response_cache:
    app.add_middleware(ResponseCacheMiddleware, cache=RESPONSE_CACHE)


# ----- Caching -----

CACHE_STATE = {"is_stale": False}


@app.middleware("http")
async def handle_cache(request: Request, call_next):
    # 1. Catch data modifications (POST, PUT, PATCH, DELETE)
    if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
        CACHE_STATE["is_stale"] = True
        return await call_next(request)

    # 2. Process the request normally
    response: Response = await call_next(request)

    # 3. Inject caching directives for successful GET requests
    if request.method == "GET" and (response.status_code == 200 or response.status_code == 204):
        if CACHE_STATE["is_stale"]:
            # Tell CapRover's Nginx to bypass its current cache file and fetch fresh data
            response.headers["X-Refresh-Cache"] = "1"
            # Reset the flag because Nginx is about to save this new fresh version
            CACHE_STATE["is_stale"] = False

        # Set a 1-hour expiration fallback limit
        response.headers["Cache-Control"] = "public, max-age=3600"

    return response


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

    db.initialize_db(reinitialize=reinitialize_database)

    if create_dummy_data:
        await db.create_dummy_data(["examples/generated_dummy_data.json"])
