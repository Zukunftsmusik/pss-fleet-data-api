from typing import Any

import pytest
from fastapi.exceptions import RequestValidationError

from src.api.exception_handlers import _raise_path_parameter_error
from src.api.models.error import RequestValidationErrorOut
from src.api.models.exceptions import ApiError, InvalidAllianceIdError, InvalidCollectionIdError, InvalidUserIdError, ServerError


test_cases = [
    # error, expected_exception
    pytest.param(
        {
            "type": "missing",
            "loc": ("path", "Random"),
            "msg": "Unexpected path parameter error",
            "input": None,
        },
        ServerError,
        id="server_error",
    ),
    pytest.param(
        {
            "type": "missing",
            "loc": ("path", "allianceId"),
            "msg": "Invalid alliance ID",
            "input": None,
        },
        InvalidAllianceIdError,
        id="alliance_id_error",
    ),
    pytest.param(
        {
            "type": "missing",
            "loc": ("path", "collectionId"),
            "msg": "Invalid collection ID",
            "input": None,
        },
        InvalidCollectionIdError,
        id="alliance_id_error",
    ),
    pytest.param(
        {
            "type": "missing",
            "loc": ("path", "userId"),
            "msg": "Invalid user ID",
            "input": None,
        },
        InvalidUserIdError,
        id="alliance_id_error",
    ),
]
"""error, expected_exception"""


@pytest.mark.parametrize(["error", "expected_exception"], test_cases)
def test__raise_path_parameter_error(error: dict[str, Any], expected_exception: ApiError):
    exc = RequestValidationError([error])
    raised_error = RequestValidationErrorOut(**error)

    with pytest.raises(expected_exception):
        _raise_path_parameter_error(raised_error, exc)
