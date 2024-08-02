from typing import Any

import pytest
from fastapi.exceptions import RequestValidationError

from src.api.exception_handlers import _raise_header_parameter_error
from src.api.models.error import RequestValidationErrorOut
from src.api.models.exceptions import ApiError, NotAuthenticatedError, ServerError


test_cases = [
    # error, expected_exception
    pytest.param(
        {
            "type": "missing",
            "loc": ("header", "Random"),
            "msg": "Field required",
            "input": None,
        },
        ServerError,
        id="server_error",
    ),
    pytest.param(
        {
            "type": "missing",
            "loc": ("header", "Authorization"),
            "msg": "Field required",
            "input": None,
        },
        NotAuthenticatedError,
        id="not_authenticated",
    ),
]
"""error, expected_exception"""


@pytest.mark.parametrize(["error", "expected_exception"], test_cases)
def test__raise_header_parameter_error(error: dict[str, Any], expected_exception: ApiError):
    exc = RequestValidationError([error])
    error = RequestValidationErrorOut(**error)

    with pytest.raises(expected_exception):
        _raise_header_parameter_error(error, exc)
