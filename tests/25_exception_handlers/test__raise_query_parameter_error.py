from typing import Any

import pytest
from fastapi.exceptions import RequestValidationError

from src.api.exception_handlers import _raise_query_parameter_error
from src.api.models.error import RequestValidationErrorOut
from src.api.models.exceptions import (
    ApiError,
    FromDateTooEarlyError,
    InvalidDescError,
    InvalidFromDateError,
    InvalidIntervalError,
    InvalidOnMissingError,
    InvalidSkipError,
    InvalidTakeError,
    InvalidToDateError,
    ServerError,
    ToDateTooEarlyError,
)


test_cases = [
    # error, expected_exception
    pytest.param(
        {
            "type": "missing",
            "loc": ("query", "Random"),
            "msg": "Unexpected query parameter error",
            "input": None,
        },
        ServerError,
        id="server_error",
    ),
    pytest.param(
        {
            "type": "missing",
            "loc": ("query", "fromDate"),
            "msg": "fromDate is missing",
            "input": None,
        },
        InvalidFromDateError,
        id="from_date_is_none",
    ),
    pytest.param(
        {
            "type": "datetime_from_date_parsing",
            "loc": ("query", "fromDate"),
            "msg": "fromDate value cannot be parsed",
            "input": "some input",
        },
        InvalidFromDateError,
        id="from_date_invalid",
    ),
    pytest.param(
        {
            "type": "too_early",
            "loc": ("query", "fromDate"),
            "msg": "fromDate too early",
            "input": "2015-01-01T00:00:00Z",
        },
        FromDateTooEarlyError,
        id="from_date_too_early",
    ),
    pytest.param(
        {
            "type": "missing",
            "loc": ("query", "toDate"),
            "msg": "toDate is missing",
            "input": None,
        },
        InvalidToDateError,
        id="to_date_is_none",
    ),
    pytest.param(
        {
            "type": "datetime_to_date_parsing",
            "loc": ("query", "toDate"),
            "msg": "toDate value cannot be parsed",
            "input": "some input",
        },
        InvalidToDateError,
        id="to_date_invalid",
    ),
    pytest.param(
        {
            "type": "to_date_too_early",
            "loc": ("query", "toDate"),
            "msg": "toDate too early",
            "input": "2015-01-01T00:00:00Z",
        },
        ToDateTooEarlyError,
        id="to_date_too_early",
    ),
    pytest.param(
        {
            "type": "query parameter",
            "loc": ("query", "interval"),
            "msg": "invalid interval",
            "input": "invalid",
        },
        InvalidIntervalError,
        id="interval_invalid",
    ),
    pytest.param(
        {
            "type": "query parameter",
            "loc": ("query", "desc"),
            "msg": "invalid desc",
            "input": "invalid",
        },
        InvalidDescError,
        id="desc_invalid",
    ),
    pytest.param(
        {
            "type": "query parameter",
            "loc": ("query", "skip"),
            "msg": "invalid skip",
            "input": "invalid",
        },
        InvalidSkipError,
        id="skip_invalid",
    ),
    pytest.param(
        {
            "type": "query parameter",
            "loc": ("query", "take"),
            "msg": "invalid take",
            "input": "invalid",
        },
        InvalidTakeError,
        id="take_invalid",
    ),
    pytest.param(
        {
            "type": "query parameter",
            "loc": ("query", "onMissing"),
            "msg": "invalid onMissing",
            "input": "on_missing_invalid",
        },
        InvalidOnMissingError,
        id="on_missing_invalid",
    ),
    pytest.param(
        {
            "type": "query parameter",
            "loc": ("query", "abcxyz"),
            "msg": "unexpected parameter",
            "input": "xyzabc",
        },
        ServerError,
        id="unexpected_parameter",
    ),
]
"""error, expected_exception"""


@pytest.mark.parametrize(["error", "expected_exception"], test_cases)
def test__raise_query_parameter_error(error: dict[str, Any], expected_exception: ApiError):
    exc = RequestValidationError([error])
    raised_error = RequestValidationErrorOut(**error)

    with pytest.raises(expected_exception):
        _raise_query_parameter_error(raised_error, exc)
