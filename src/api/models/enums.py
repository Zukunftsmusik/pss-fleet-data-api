from enum import IntEnum, StrEnum


class ErrorCode(StrEnum):
    """
    An error code returned by the API when an error occurs.
    """

    ALLIANCE_NOT_FOUND = "ALLIANCE_NOT_FOUND"
    COLLECTION_NOT_DELETED = "COLLECTION_NOT_DELETED"
    COLLECTION_NOT_FOUND = "COLLECTION_NOT_FOUND"
    CONFLICT = "CONFLICT"
    FORBIDDEN = "FORBIDDEN"
    FROM_DATE_AFTER_TO_DATE = "FROM_DATE_AFTER_TO_DATE"
    INVALID_BOOL = "INVALID_BOOL"
    INVALID_DATETIME = "INVALID_DATETIME"
    INVALID_JSON_FORMAT = "INVALID_JSON_FORMAT"
    INVALID_NUMBER = "INVALID_NUMBER"
    INVALID_PARAMETER = "INVALID_PARAMETER"
    INVALID_PARAMETER_FORMAT = "INVALID_PARAMETER_FORMAT"
    INVALID_PARAMETER_VALUE = "INVALID_PARAMETER_VALUE"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    NON_UNIQUE_COLLECTION_ID = "NOT_UNIQUE_COLLECTION_ID"
    NON_UNIQUE_TIMESTAMP = "NON_UNIQUE_TIMESTAMP"
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"
    NOT_FOUND = "NOT_FOUND"
    PARAMETER_ALLIANCE_ID_INVALID = "PARAMETER_ALLIANCE_ID_INVALID"
    PARAMETER_COLLECTION_ID_INVALID = "PARAMETER_COLLECTION_ID_INVALID"
    PARAMETER_DESC_INVALID = "PARAMETER_DESC_INVALID"
    PARAMETER_FROM_DATE_INVALID = "PARAMETER_FROM_DATE_INVALID"
    PARAMETER_FROM_DATE_TOO_EARLY = "PARAMETER_FROM_DATE_TOO_EARLY"
    PARAMETER_INTERVAL_INVALID = "PARAMETER_INTERVAL_INVALID"
    PARAMETER_SKIP_INVALID = "PARAMETER_SKIP_INVALID"
    PARAMETER_TAKE_INVALID = "PARAMETER_TAKE_INVALID"
    PARAMETER_TO_DATE_INVALID = "PARAMETER_TO_DATE_INVALID"
    PARAMETER_TO_DATE_TOO_EARLY = "PARAMETER_TO_DATE_TOO_EARLY"
    PARAMETER_USER_ID_INVALID = "PARAMETER_USER_ID_INVALID"
    RATE_LIMITED = "RATE_LIMITED"
    SCHEMA_VERSION_MISMATCH = "SCHEMA_VERSION_MISMATCH"
    SERVER_ERROR = "SERVER_ERROR"
    UNSUPPORTED_MEDIA_TYPE = "UNSUPPORTED_MEDIA_TYPE"
    UNSUPPORTED_SCHEMA = "UNSUPPORTED_SCHEMA"
    USER_NOT_FOUND = "USER_NOT_FOUND"


class OperationId(StrEnum):
    """
    An `operation_id` of an API endpoint.
    """

    CREATE_COLLECTION = "CreateCollection"
    DELETE_COLLECTION = "DeleteCollection"
    GET_ALLIANCE_HISTORY = "GetAllianceHistory"
    GET_COLLECTION = "GetCollection"
    GET_COLLECTIONS = "GetCollections"
    GET_ALLIANCE_FROM_COLLECTION = "GetAllianceFromCollection"
    GET_ALLIANCES_FROM_COLLECTION = "GetAlliancesFromCollection"
    GET_HOME_PAGE = "GetHomePage"
    GET_TOP_100_USERS_FROM_COLLECTION = "GetTop100UsersFromCollection"
    GET_USER_FROM_COLLECTION = "GetUserFromCollection"
    GET_USERS_FROM_COLLECTION = "GetUsersFromCollection"
    GET_USER_HISTORY = "GetUserHistory"
    UPLOAD_COLLECTION = "UploadCollection"


class ParameterInterval(StrEnum):
    """
    The interval of history data to be returned.
    """

    HOURLY = "hour"
    """Return hourly data recorded 1 minute before a given full hour, if possible. Hourly data may not be available."""
    DAILY = "day"
    """Return daily data recorded 1 minute before daily reset, if possible. Daily data may not be available."""
    MONTHLY = "month"
    """Return monthly data recorded 1 minute before monthly reset, if possible. Monthly data may not be available."""


class UserAllianceMembership(StrEnum):
    """
    Denotes the rank of a fleet member in PSS.
    """

    NONE = "None"
    """This User is not member of an Alliance."""
    FLEET_ADMIRAL = "FleetAdmiral"
    """This User is of rank Fleet Admiral."""
    VICE_ADMIRAL = "ViceAdmiral"
    """This User is of rank Vice Admiral."""
    COMMANDER = "Commander"
    """This User is of rank Commander."""
    MAJOR = "Major"
    """This User is of rank Major."""
    LIEUTENANT = "Lieutenant"
    """This User is of rank Lieutenant."""
    ENSIGN = "Ensign"
    """This User is of rank Ensign."""
    CANDIDATE = "Candidate"
    """This User is of rank Candidate."""


class UserAllianceMembershipEncoded(IntEnum):
    """
    Denotes the rank of a fleet member in PSS, encoded as an `int` to save space.
    """

    NONE = -1
    """This User is not member of an Alliance."""
    FLEET_ADMIRAL = 0
    """This User is of rank Fleet Admiral."""
    VICE_ADMIRAL = 1
    """This User is of rank Vice Admiral."""
    COMMANDER = 2
    """This User is of rank Commander."""
    MAJOR = 3
    """This User is of rank Major."""
    LIEUTENANT = 4
    """This User is of rank Lieutenant."""
    ENSIGN = 5
    """This User is of rank Ensign."""
    CANDIDATE = 6
    """This User is of rank Candidate."""


__all__ = [
    ErrorCode.__name__,
    OperationId.__name__,
    ParameterInterval.__name__,
    UserAllianceMembership.__name__,
    UserAllianceMembershipEncoded.__name__,
]
