from typing import Any

from fastapi import status

from ..models.error import ErrorConverter, ErrorOut
from ..models.exceptions import (
    ConflictError,
    MethodNotAllowedError,
    MissingAccessError,
    NotAuthenticatedError,
    NotFoundError,
    ParameterValidationError,
    ServerError,
    TooManyRequestsError,
    UnsupportedMediaTypeError,
)


def get_default_responses(*status_codes: int) -> dict[int, dict[str, Any]]:
    """Returns the default responses for the specified HTTP status codes.

    Returns:
        dict[int, dict[str, Any]]: A dictionary with HTTP status codes as keys and their respective default response as values.
    """
    all_codes = all_default_responses.keys()
    status_codes = [status_code for status_code in status_codes if status_code in all_codes]

    result = {status_code: all_default_responses[status_code] for status_code in status_codes}
    return result


def get_default_responses_for_get(
    include_204: bool = False, description_204: str = None, include_404: bool = False, description_404: str = None
) -> dict[int, dict[str, Any]]:
    """Returns responses for HTTP status codes 405, 422, 429 & 500. Optionally includes 204 & 404.

    Args:
        include_204 (bool, optional): Include a response for HTTP status code 204. Defaults to False.
        description_204 (str, optional): Override the response description for the HTTP status code 204 response. Defaults to None.
        include_404 (bool, optional): Include a response for HTTP status code 404. Defaults to False.
        description_404 (str, optional): Override the response description for the HTTP status code 404 response. Defaults to None.

    Returns:
        dict[int, dict[str, Any]]: A dictionary with HTTP status codes as keys and their respective default response as values.
    """
    status_codes = [
        status.HTTP_405_METHOD_NOT_ALLOWED,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        status.HTTP_429_TOO_MANY_REQUESTS,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    if include_204:
        status_codes.append(status.HTTP_204_NO_CONTENT)
    if include_404:
        status_codes.append(status.HTTP_404_NOT_FOUND)
    result = get_default_responses(*status_codes)

    if include_204 and description_204:
        result[status.HTTP_204_NO_CONTENT]["description"] = description_204
    if include_404 and description_404:
        result[status.HTTP_404_NOT_FOUND]["description"] = description_404

    return result


all_default_responses = {
    status.HTTP_204_NO_CONTENT: {
        "model": None,
        "description": "There is no data for the specified parameters.",
        "content": {
            "application/json": {
                "schema": {
                    "example": [],
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorOut,
        "description": "The client is not authenticated.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "ErrorOut",
                    "example": ErrorConverter.to_error_out(
                        NotAuthenticatedError("The client is not authenticated.", suggestion="Authenticate yourself."), "{endpointUrl}"
                    ).model_dump_json(),
                }
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "model": ErrorOut,
        "description": "The client is not authorized.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "ErrorOut",
                    "example": ErrorConverter.to_error_out(MissingAccessError("The client is not authorized."), "{endpointUrl}").model_dump_json(),
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorOut,
        "description": "The requested resource was not found.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "ErrorOut",
                    "example": ErrorConverter.to_error_out(NotFoundError("The requested resource was not found."), "{endpointUrl}").model_dump_json(),
                }
            }
        },
    },
    status.HTTP_405_METHOD_NOT_ALLOWED: {
        "model": ErrorOut,
        "description": "The method is not allowed for this endpoint.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "ErrorOut",
                    "example": ErrorConverter.to_error_out(
                        MethodNotAllowedError("The method is not allowed for this endpoint."), "{endpointUrl}"
                    ).model_dump_json(),
                }
            }
        },
    },
    status.HTTP_409_CONFLICT: {
        "model": ErrorOut,
        "description": "The resource can't be created in this form.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "ErrorOut",
                    "example": ErrorConverter.to_error_out(
                        ConflictError("The resource can't be created in this form."), "{endpointUrl}"
                    ).model_dump_json(),
                }
            }
        },
    },
    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {
        "model": ErrorOut,
        "description": "The media type is not supported.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "ErrorOut",
                    "example": ErrorConverter.to_error_out(
                        UnsupportedMediaTypeError("The media type is not supported."), "{endpointUrl}"
                    ).model_dump_json(),
                }
            }
        },
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": ErrorOut,
        "description": "A parameter received an invalid value.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "ErrorOut",
                    "example": ErrorConverter.to_error_out(
                        ParameterValidationError("A parameter received an invalid value.", suggestion="Do this or that to fix the issue."),
                        "{endpointUrl}",
                    ).model_dump_json(),
                }
            }
        },
    },
    status.HTTP_429_TOO_MANY_REQUESTS: {
        "model": ErrorOut,
        "description": "You have been rate-limited.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "ErrorOut",
                    "example": ErrorConverter.to_error_out(
                        TooManyRequestsError("The requested resource was not found.", suggestion="Please try again in: x seconds"), "{endpointUrl}"
                    ).model_dump_json(),
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": ErrorOut,
        "description": "An error occured on the server while processing this request.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "ErrorOut",
                    "example": ErrorConverter.to_error_out(ServerError("Oops. Success!"), "{endpointUrl}").model_dump_json(),
                }
            }
        },
    },
}


__all__ = [
    get_default_responses.__name__,
    get_default_responses_for_get.__name__,
]
