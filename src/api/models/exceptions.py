from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Union

from ..models.enums import ErrorCode
from .link import Link


# Base Exception


@dataclass(frozen=True)
class ApiError(Exception):
    """
    The base exception to be thrown, when an error occurs in the API.
    """

    code: Union[str, ErrorCode] = field(init=False)
    message: str = field(init=False)
    details: str
    timestamp: Union[datetime, str] = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    suggestion: str = field(default="")
    links: list[Link] = field(default_factory=lambda: list())


# HTTP 401


class NotAuthenticatedError(ApiError):
    code = ErrorCode.NOT_AUTHENTICATED
    message = "You are not authenticated."


# HTTP 403


class MissingAccessError(ApiError):
    code = ErrorCode.FORBIDDEN
    message = "You don't have the required permissions to access this endpoint."


# HTTP 404


class NotFoundError(ApiError):
    code = ErrorCode.NOT_FOUND
    message = "The requested resource could not be found."


class AllianceNotFoundError(NotFoundError):
    code = ErrorCode.ALLIANCE_NOT_FOUND
    message = "The requested Alliance could not be found."


class CollectionNotFoundError(NotFoundError):
    code = ErrorCode.COLLECTION_NOT_FOUND
    message = "The requested Collection could not be found."


class UserNotFoundError(NotFoundError):
    code = ErrorCode.USER_NOT_FOUND
    message = "The requested User could not be found."


# HTTP 405


class MethodNotAllowedError(ApiError):
    code = ErrorCode.METHOD_NOT_ALLOWED
    message = "The method is not allowed for this endpoint."


# HTTP 409


class ConflictError(ApiError):
    code = ErrorCode.CONFLICT
    message = "The resource could not be created or updated."


class NonUniqueTimestampError(ConflictError):
    code = ErrorCode.NON_UNIQUE_TIMESTAMP
    message: str = f"{ConflictError.message}: A Collection with this timestamp already exists."


class NonUniqueCollectionIdError(ConflictError):
    code = ErrorCode.NON_UNIQUE_COLLECTION_ID
    message: str = f"{ConflictError.message}: A Collection with this collectionId already exists."


# HTTP 415


class UnsupportedMediaTypeError(ApiError):
    code = ErrorCode.UNSUPPORTED_MEDIA_TYPE
    message = "The provided media type is not supported."


# HTTP 422


class ParameterValidationError(ApiError):
    code = ErrorCode.INVALID_PARAMETER
    message = "A provided parameter received an unsupported value or is in an unsupported format."


# Parameter Format


class ParameterFormatError(ParameterValidationError):
    code = ErrorCode.INVALID_PARAMETER_FORMAT
    message = "A provided parameter is in an unsupported format."


class InvalidBoolError(ParameterFormatError):
    code = ErrorCode.INVALID_BOOL
    message = "The provided value can't be parsed to a bool."


class InvalidDateTimeError(ParameterFormatError):
    code = ErrorCode.INVALID_DATETIME
    message = "The provided value can't be parsed to a datetime."


class InvalidJsonUpload(ParameterFormatError):
    code = ErrorCode.INVALID_JSON_FORMAT
    message = "The uploaded file is not a valid json file."


class InvalidNumberError(ParameterFormatError):
    code = ErrorCode.INVALID_NUMBER
    message = "The provided value can't be parsed to a number."


class UnsupportedSchemaError(ParameterFormatError):
    code = ErrorCode.UNSUPPORTED_SCHEMA
    message = "The provided Collection is of an unsupported schema."


class SchemaVersionMismatch(UnsupportedSchemaError):
    code = ErrorCode.SCHEMA_VERSION_MISMATCH
    message = "The file contents don't match the declared schema version."


# Parameter Value


class ParameterValueError(ParameterValidationError):
    code = ErrorCode.INVALID_PARAMETER_VALUE
    message = "A provided parameter received an unsupported value."


class FromDateAfterToDateError(ParameterValueError):
    code = ErrorCode.FROM_DATE_AFTER_TO_DATE
    message = "The value for the parameter `fromDate` is bigger than the value for the parameter `toDate`."


class InvalidAllianceIdError(ParameterValueError):
    code = ErrorCode.PARAMETER_ALLIANCE_ID_INVALID
    message = "The provided value for the parameter `allianceId` is invalid."


class InvalidCollectionIdError(ParameterValueError):
    code = ErrorCode.PARAMETER_COLLECTION_ID_INVALID
    message = "The provided value for the parameter `collectionId` is invalid."


class InvalidDescError(ParameterValueError):
    code = ErrorCode.PARAMETER_DESC_INVALID
    message = "The provided value for the parameter `desc` is invalid."


class InvalidFromDateError(ParameterValueError):
    code = ErrorCode.PARAMETER_FROM_DATE_INVALID
    message = "The provided value for the parameter `fromDate` is invalid."


class FromDateTooEarlyError(InvalidFromDateError):
    code = ErrorCode.PARAMETER_FROM_DATE_TOO_EARLY
    message = "The provided value for the parameter `fromDate` is too early."


class InvalidToDateError(ParameterValueError):
    code = ErrorCode.PARAMETER_TO_DATE_INVALID
    message = "The provided value for the parameter `toDate` is invalid."


class ToDateTooEarlyError(InvalidToDateError):
    code = ErrorCode.PARAMETER_TO_DATE_TOO_EARLY
    message = "The provided value for the parameter `toDate` is too early."


class InvalidIntervalError(ParameterValueError):
    code = ErrorCode.PARAMETER_INTERVAL_INVALID
    message = "The provided value for the parameter `interval` is invalid."


class InvalidSkipError(ParameterValueError):
    code = ErrorCode.PARAMETER_SKIP_INVALID
    message = "The provided value for the parameter `skip` is invalid."


class InvalidTakeError(ParameterValueError):
    code = ErrorCode.PARAMETER_TAKE_INVALID
    message = "The provided value for the parameter `take` is invalid."


class InvalidUserIdError(ParameterValueError):
    code = ErrorCode.PARAMETER_USER_ID_INVALID
    message = "The provided value for the parameter `userId` is invalid."


# HTTP 429


class TooManyRequestsError(ApiError):  # 429
    code = ErrorCode.RATE_LIMITED
    message = "You've been rate-limited."


# HTTP 500


class ServerError(ApiError):  # 500
    code = ErrorCode.SERVER_ERROR
    message = "An internal server error occured."


class CollectionNotDeletedError(ServerError):
    code = ErrorCode.COLLECTION_NOT_DELETED
    message = "The requested Collection could not be deleted."


__all__ = [
    AllianceNotFoundError.__name__,
    ApiError.__name__,
    CollectionNotDeletedError.__name__,
    CollectionNotFoundError.__name__,
    ConflictError.__name__,
    FromDateAfterToDateError.__name__,
    FromDateTooEarlyError.__name__,
    InvalidAllianceIdError.__name__,
    InvalidBoolError.__name__,
    InvalidCollectionIdError.__name__,
    InvalidDateTimeError.__name__,
    InvalidDescError.__name__,
    InvalidFromDateError.__name__,
    InvalidIntervalError.__name__,
    InvalidJsonUpload.__name__,
    InvalidNumberError.__name__,
    InvalidSkipError.__name__,
    InvalidTakeError.__name__,
    InvalidToDateError.__name__,
    InvalidUserIdError.__name__,
    MethodNotAllowedError.__name__,
    MissingAccessError.__name__,
    NonUniqueCollectionIdError.__name__,
    NonUniqueTimestampError.__name__,
    NotAuthenticatedError.__name__,
    NotFoundError.__name__,
    ParameterFormatError.__name__,
    ParameterValidationError.__name__,
    ParameterValueError.__name__,
    SchemaVersionMismatch.__name__,
    ServerError.__name__,
    ToDateTooEarlyError.__name__,
    TooManyRequestsError.__name__,
    UnsupportedMediaTypeError.__name__,
    UnsupportedSchemaError.__name__,
    UserNotFoundError.__name__,
]
