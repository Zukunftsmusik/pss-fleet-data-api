from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import SETTINGS
from .database import db
from .models.error import ErrorConverter, RequestValidationErrorOut
from .models.exceptions import (
    ApiError,
    ConflictError,
    FromDateTooEarlyError,
    InvalidAllianceIdError,
    InvalidCollectionIdError,
    InvalidDescError,
    InvalidFromDateError,
    InvalidIntervalError,
    InvalidSkipError,
    InvalidTakeError,
    InvalidToDateError,
    InvalidUserIdError,
    MethodNotAllowedError,
    MissingAccessError,
    NotAuthenticatedError,
    NotFoundError,
    ParameterValidationError,
    ServerError,
    UnsupportedSchemaError,
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


async def handle_api_error(request: Request, exception: ApiError, status_code: int) -> ORJSONResponse:
    """Converts an `ApiError` to a proper error response and returns it with the appropriate HTTP status code.

    Args:
        request (Request): The request that produced the exception.
        exception (ApiError): The exception that was thrown.
        status_code (int): The HTTP status code to be returned.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    error_out = ErrorConverter.to_error_out(exception, str(request.url))
    return ORJSONResponse(dict(error_out), status_code=status_code)


@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(request: Request, exc: StarletteHTTPException) -> ORJSONResponse:
    """Handles a generic starlette `HTTPException` depending on its `status_code`.

    Args:
        request (Request): The request that produced the exception.
        exc (HTTPException): The exception that was thrown.

    Raises:
        exc: The exception that was thrown, if it isn't being handled by this function.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    match exc.status_code:
        case status.HTTP_405_METHOD_NOT_ALLOWED:
            return await handle_api_error(
                request,
                MethodNotAllowedError(f"The method '{request.method}' is not allowed for this endpoint."),
                exc.status_code,
            )
    raise exc


@app.exception_handler(NotAuthenticatedError)
async def handle_not_authenticated(request: Request, exception: NotAuthenticatedError) -> ORJSONResponse:
    """Handles a `NotAuthenticatedError` (401) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (NotAuthenticatedError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await handle_api_error(request, exception, status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(MissingAccessError)
async def handle_missing_access(request: Request, exception: MissingAccessError) -> ORJSONResponse:
    """Handles a `MissingAccessError` (403) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (MissingAccessError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await handle_api_error(request, exception, status.HTTP_403_FORBIDDEN)


@app.exception_handler(NotFoundError)
async def handle_not_found(request: Request, exception: NotFoundError) -> ORJSONResponse:
    """Handles any `NotFoundError` (404) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (NotFoundError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await handle_api_error(request, exception, status.HTTP_404_NOT_FOUND)


@app.exception_handler(MethodNotAllowedError)
async def handle_method_not_allowed(request: Request, exception: MethodNotAllowedError) -> ORJSONResponse:
    """Handles a `MethodNotAllowedError` (405) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (MethodNotAllowedError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await handle_api_error(request, exception, status.HTTP_405_METHOD_NOT_ALLOWED)


@app.exception_handler(ConflictError)
async def handle_conflict(request: Request, exception: ConflictError) -> ORJSONResponse:
    """Handles any `ConflictError` (409) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (ConflictError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await handle_api_error(request, exception, status.HTTP_409_CONFLICT)


@app.exception_handler(ParameterValidationError)
async def handle_parameter_validation(request: Request, exception: ParameterValidationError) -> ORJSONResponse:
    """Handles any `ParameterValidationError` (422) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (ParameterValidationError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await handle_api_error(request, exception, status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.exception_handler(ServerError)
async def handle_server(request: Request, exception: ServerError) -> ORJSONResponse:
    """Handles any `ServerError` (500) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (ServerError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await handle_api_error(request, exception, status.HTTP_500_INTERNAL_SERVER_ERROR)


def _raise_nested_body_parameter_error(error: RequestValidationErrorOut):
    """Handles a `RequestValidationError` (422) raised upon a failed validation of a nested body parameter and raises an appropriate detailed exception to be handled.

    Args:
        error (RequestValidationErrorOut): Details of the `RequestValidationError` that was thrown.

    Raises:
        UnsupportedSchemaError: Raised, if:
          - The representation of an Alliance is not valid.
          - A tuple representing an Alliance is missing one or more values.
          - A field is missing from a Collection's metadata.
          - The `timestamp` in a Collection's metadata has no value.
          - The `timestamp` in a Collection's metadata received a value that can't be parsed to a `datetime`.
          - The representation of a User is not valid.
          - A tuple representing a User is missing one or more values.
          - The representation of a User received a value for `AllianceMembership` that can't be parsed to an `AllianceMembership` value.
          - The representation of a User received a value for `AllianceJoinDate`, `LastLoginDate` or `LastHeartBeatDate` that can't be parsed to a `datetime` value.
    """
    match error.param_path[0]:
        case "fleets":
            if error.type == "too_long":
                fleet_index = error.loc[-1]
                raise UnsupportedSchemaError(f"The fleet at index {fleet_index} is not a valid representation.", suggestion=error.msg)
            if error.type == "missing":
                fleet_index = error.loc[-2]
                raise UnsupportedSchemaError(f"The fleet at index {fleet_index} is missing one or more values.")
        case "metadata":
            if error.type == "missing":
                raise UnsupportedSchemaError(f"The field {error.param_name} is missing from the metadata.")
            match error.param_name:
                case "timestamp":
                    if error.input is None:
                        raise UnsupportedSchemaError("The provided schema does not contain a 'timestamp'.")
                    raise UnsupportedSchemaError("The provided 'timestamp' is invalid.", suggestion=error.msg)
        case "users":
            user_index = error.loc[-2]
            match error.type:
                case "too_long":
                    user_index = error.loc[-1]
                    raise UnsupportedSchemaError(f"The user at index {user_index} is not a valid representation.", suggestion=error.msg)
                case "missing":
                    raise UnsupportedSchemaError(f"The user at index {user_index} is missing one or more values.")

            error_index = error.loc[-1]
            match error_index:
                case 5:
                    field_name = "AllianceMembership"
                case 6:
                    field_name = "AllianceJoinDate"
                case 7:
                    field_name = "LastLoginDate"
                case 8:
                    field_name = "LastHeartBeatDate"
            raise UnsupportedSchemaError(
                f"The user at index {user_index} received an unsupported value for field '{field_name}' (at position: {error_index}).",
                suggestion=error.msg,
            )


def _raise_non_nested_body_parameter_error(error: RequestValidationErrorOut):
    """Handles a `RequestValidationError` (422) raised upon a failed validation of a flat (non-nested) body parameter and raises an appropriate detailed exception to be handled.

    Args:
        error (RequestValidationErrorOut): Details of the `RequestValidationError` that was thrown.

    Raises:
        UnsupportedSchemaError: Raised, if:
          - The body is missing the field `fleets`.
          - The field `fleets` in the body is `None`.
          - The body is missing the field `metadata`.
          - The body is missing the field `users`.
          - The field `users` in the body is `None`.
    """
    match error.param_name:
        case "fleets":
            if error.type == "missing":
                raise UnsupportedSchemaError(
                    "The provided schema does not include the list of fleets.",
                    suggestion="Add the field 'fleets' to the Collection. If no fleets were collected, add an empty list.",
                )
            if error.input is None:
                raise UnsupportedSchemaError(
                    "The provided schema does not include the list of fleets.", suggestion="If no fleets were collected, add an empty list."
                )
        case "metadata":
            if error.type == "missing" or error.input is None:
                raise UnsupportedSchemaError("The provided schema does not include any metadata.", suggestion="Add metadata to the Collection.")
        case "users":
            if error.type == "missing":
                raise UnsupportedSchemaError(
                    "The provided schema does not include the list of users.",
                    suggestion="Add the field 'users' to the Collection. If no users were collected, add an empty list.",
                )
            if error.input is None:
                raise UnsupportedSchemaError(
                    "The provided schema does not include the list of users.", suggestion="If no users were collected, add an empty list."
                )


def _raise_body_parameter_error(error: RequestValidationErrorOut):
    """Handles a `RequestValidationError` (422) raised upon a failed validation of a body parameter and raises an appropriate detailed exception to be handled.

    Args:
        error (RequestValidationErrorOut): _description_

    Raises:
        See functions `_raise_nested_body_parameter_error` and `_raise_non_nested_body_parameter_error`.
        ServerError: Raised, if the functions mentioned above don't raise an exception.
    """
    if error.param_path:
        _raise_nested_body_parameter_error(error)
    else:
        _raise_non_nested_body_parameter_error(error)
    raise ServerError("An error occured while raising an error for an invalid body parameter.")


def _raise_path_parameter_error(error: RequestValidationErrorOut):
    """Handles a `RequestValidationError` (422) raised upon a failed validation of a path parameter and raises an appropriate detailed exception to be handled.

    Args:
        error (RequestValidationErrorOut): Details of the `RequestValidationError` that was thrown.

    Raises:
        InvalidAllianceIdError: Raised, if the path parameter `allianceId` received a value that can't be parsed to an `int` or is lower than 1.
        InvalidCollectionIdError: Raised, if the path parameter `collectionId` received a value that can't be parsed to an `int` or is lower than 1.
        InvalidUserIdError: Raised, if the path parameter `userId` received a value that can't be parsed to an `int` or is lower than 1.
        ServerError: Raised, if none of the other exceptions was raised.
    """
    match error.param_name:
        case "allianceId":
            raise InvalidAllianceIdError(error.msg)
        case "collectionId":
            raise InvalidCollectionIdError(error.msg)
        case "userId":
            raise InvalidUserIdError(error.msg)
    raise ServerError("An error occured while raising an error for an invalid path parameter.")


def _raise_query_parameter_error(error: RequestValidationErrorOut):
    """Handles a `RequestValidationError` (422) raised upon a failed validation of a query parameter and raises an appropriate detailed exception to be handled.

    Args:
        error (RequestValidationErrorOut): Details of the `RequestValidationError` that was thrown.

    Raises:
        InvalidFromDateError: Raised, if the query parameter `fromDate` received a value that can't be parsed to a `datetime`.
        FromDateTooEarlyError: Raised, if the query parameter `fromDate` received a value that is before the PSS start date.
        InvalidToDateError: Raised, if the query parameter `toDate` received a value that can't be parsed to a `datetime`.
        InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to a `ParameterInterval` enum value.
        InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to a `bool`.
        InvalidSkipError: Raised, if the query parameter `skip` received a value that can't be parsed to an `int` or if it's negative.
        InvalidTakeError: Raised, if the query parameter `skip` received a value that can't be parsed to an `int`, if it's negative or if it's greater than 100.
        ServerError: Raised, if none of the other exceptions was raised.
    """
    match error.param_name:
        case "fromDate":
            if not error.input or error.type == "datetime_from_date_parsing":
                raise InvalidFromDateError(error.msg)
            raise FromDateTooEarlyError(error.msg)
        case "toDate":
            if not error.input or error.type == "datetime_from_date_parsing":
                raise InvalidToDateError(error.msg)
        case "interval":
            raise InvalidIntervalError(error.msg)
        case "desc":
            raise InvalidDescError(error.msg)
        case "skip":
            raise InvalidSkipError(error.msg)
        case "take":
            raise InvalidTakeError(error.msg)
    raise ServerError("An error occured while raising an error for an invalid query parameter.")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles any `RequestValidationError` (422) thrown from within an API endpoint and raises an appropriate detailed exception to be handled.

    Args:
        request (Request): The request that produced the exception.
        exc (RequestValidationError): The exception that was thrown.

    Raises:
        See functions `_raise_path_parameter_error`, `_raise_query_parameter_error` and `_raise_body_parameter_error`.
    """
    error = RequestValidationErrorOut(**exc._errors[0])
    match error.param_location:
        case "path":
            _raise_path_parameter_error(error)
        case "query":
            _raise_query_parameter_error(error)
        case "body":
            _raise_body_parameter_error(error)
