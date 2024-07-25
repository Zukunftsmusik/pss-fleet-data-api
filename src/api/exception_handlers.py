from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

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
    ToDateTooEarlyError,
    UnsupportedSchemaError,
)


# Exception handler functions


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
            return await _handle_api_error(
                request,
                MethodNotAllowedError(f"The method '{request.method}' is not allowed for this endpoint."),
                exc.status_code,
            )
    raise exc


async def handle_not_authenticated(request: Request, exception: NotAuthenticatedError) -> ORJSONResponse:
    """Handles a `NotAuthenticatedError` (401) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (NotAuthenticatedError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await _handle_api_error(request, exception, status.HTTP_401_UNAUTHORIZED)


async def handle_missing_access(request: Request, exception: MissingAccessError) -> ORJSONResponse:
    """Handles a `MissingAccessError` (403) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (MissingAccessError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await _handle_api_error(request, exception, status.HTTP_403_FORBIDDEN)


async def handle_not_found(request: Request, exception: NotFoundError) -> ORJSONResponse:
    """Handles any `NotFoundError` (404) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (NotFoundError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await _handle_api_error(request, exception, status.HTTP_404_NOT_FOUND)


async def handle_method_not_allowed(request: Request, exception: MethodNotAllowedError) -> ORJSONResponse:
    """Handles a `MethodNotAllowedError` (405) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (MethodNotAllowedError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await _handle_api_error(request, exception, status.HTTP_405_METHOD_NOT_ALLOWED)


async def handle_conflict(request: Request, exception: ConflictError) -> ORJSONResponse:
    """Handles any `ConflictError` (409) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (ConflictError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await _handle_api_error(request, exception, status.HTTP_409_CONFLICT)


async def handle_parameter_validation(request: Request, exception: ParameterValidationError) -> ORJSONResponse:
    """Handles any `ParameterValidationError` (422) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (ParameterValidationError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await _handle_api_error(request, exception, status.HTTP_422_UNPROCESSABLE_ENTITY)


async def handle_request_validation(request: Request, exc: RequestValidationError):
    """Handles any `RequestValidationError` (422) thrown from within an API endpoint and raises an appropriate detailed exception to be handled.

    Args:
        request (Request): The request that produced the exception.
        exc (RequestValidationError): The exception that was thrown.

    Raises:
        See functions `_raise_body_parameter_error`, `_raise_header_parameter_error`, `_raise_path_parameter_error` & `_raise_query_parameter_error`.
        ServerError: Raised, if the functions mentioned above don't raise an exception.
    """
    error = RequestValidationErrorOut(**exc._errors[0])
    match error.param_location:
        case "body":
            _raise_body_parameter_error(error, exc)
        case "header":
            _raise_header_parameter_error(error, exc)
        case "path":
            _raise_path_parameter_error(error, exc)
        case "query":
            _raise_query_parameter_error(error, exc)
    raise ServerError("An error occured while raising an error for an invalid parameter.") from exc


async def handle_server(request: Request, exception: ServerError) -> ORJSONResponse:
    """Handles any `ServerError` (500) thrown from within an API endpoint.

    Args:
        request (Request): The request that produced the exception.
        exception (ServerError): The exception that was thrown.

    Returns:
        ORJSONResponse: The response to be returned to the client.
    """
    return await _handle_api_error(request, exception, status.HTTP_500_INTERNAL_SERVER_ERROR)


# Helper functions


async def _handle_api_error(request: Request, exception: ApiError, status_code: int) -> ORJSONResponse:
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


def _raise_body_parameter_error(error: RequestValidationErrorOut, exc: RequestValidationError):
    """Handles a `RequestValidationError` (422) raised upon a failed validation of a body parameter and raises an appropriate detailed exception to be handled.

    Args:
        error (RequestValidationErrorOut): Details of the `RequestValidationError` that was thrown.

    Raises:
        See functions `_raise_nested_body_parameter_error` and `_raise_non_nested_body_parameter_error`.
        ServerError: Raised, if the functions mentioned above don't raise an exception.
    """
    if error.param_path:
        _raise_nested_body_parameter_error(error, exc)
    else:
        _raise_non_nested_body_parameter_error(error, exc)
    raise ServerError("An error occured while raising an error for an invalid body parameter.") from exc


def _raise_header_parameter_error(error: RequestValidationErrorOut, exc: RequestValidationError):
    """Handles a `RequestValidationError` (422) raised upon a failed validation of a header parameter and raises an appropriate detailed exception to be handled.

    Args:
        error (RequestValidationErrorOut): Details of the `RequestValidationError` that was thrown.

    Raises:
        ServerError: Raised, if the functions mentioned above don't raise an exception.
    """
    match error.param_name:
        case "Authorization":
            raise NotAuthenticatedError(
                "'Authorization' header not found in request.", suggestion="Add an 'Authorization' header to the request with an authorized api key."
            )
    raise ServerError("An error occured while raising an error for an invalid header parameter.") from exc


def _raise_nested_body_parameter_error(error: RequestValidationErrorOut, exc: RequestValidationError):
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
        case "meta":
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


def _raise_non_nested_body_parameter_error(error: RequestValidationErrorOut, exc: RequestValidationError):
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
        case "meta":
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


def _raise_path_parameter_error(error: RequestValidationErrorOut, exc: RequestValidationError):
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
    raise ServerError("An error occured while raising an error for an invalid path parameter.") from exc


def _raise_query_parameter_error(error: RequestValidationErrorOut, exc: RequestValidationError):
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
            raise ToDateTooEarlyError(error.msg)
        case "interval":
            raise InvalidIntervalError(error.msg)
        case "desc":
            raise InvalidDescError(error.msg)
        case "skip":
            raise InvalidSkipError(error.msg)
        case "take":
            raise InvalidTakeError(error.msg)
    raise ServerError("An error occured while raising an error for an invalid query parameter.") from exc
