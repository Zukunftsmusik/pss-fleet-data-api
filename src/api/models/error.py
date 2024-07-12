from typing import Any, Optional, Union

from pydantic import BaseModel

from .. import utils
from .exceptions import ApiError
from .link import Link


class ErrorOut(BaseModel):
    """
    Represents an Error sent to the client in the case of an exception.
    """

    code: str
    message: str
    details: str
    timestamp: str
    url: str
    suggestion: str
    links: list[Link]


class RequestValidationErrorOut(BaseModel):
    """
    Represents a RequestValidationError used to send an Error to the client in the case of an exception.
    """

    type: str
    loc: tuple[Union[int, str], ...]
    msg: str
    input: Optional[Any]
    ctx: Optional[dict[str, Any]] = None

    @property
    def param_location(self) -> str:
        return self.loc[0]

    @property
    def param_name(self) -> str:
        return self.loc[-1]

    @property
    def param_path(self) -> tuple[str, ...]:
        return tuple(self.loc[1:-1])


class ErrorConverter:
    """
    Convert an ApiError instance.
    """

    @staticmethod
    def to_error_out(error: ApiError, url: str) -> "ErrorOut":
        """Converts an `ApiError` to a user-friendly format to be returned in a response.

        Args:
            error (ApiError): The exception that occured.
            url (str): The URL of the endpoint that raised the exception.

        Returns:
            ErrorOut: A human-readable error object.
        """
        if isinstance(error.timestamp, str):
            timestamp = utils.parse_datetime(error.timestamp)
        else:
            timestamp = error.timestamp
        return ErrorOut(
            code=str(error.code),
            message=error.message,
            details=error.details,
            timestamp=f"{timestamp.isoformat()}",
            url=url,
            suggestion=error.suggestion or "",
            links=error.links or [],
        )


__all__ = [
    ErrorConverter.__name__,
    ErrorOut.__name__,
    RequestValidationErrorOut.__name__,
]
