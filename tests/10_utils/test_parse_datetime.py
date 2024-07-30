from contextlib import AbstractContextManager
from datetime import datetime, timezone
from typing import Any, Optional, Union

import pytest

from src.api.utils import parse_datetime


test_cases_invalid = [
    # value, expected_exception
    pytest.param(True, pytest.raises(TypeError), id="bool"),
    pytest.param(12.34, pytest.raises(TypeError), id="float"),
    pytest.param(complex("-1.23+4.5j"), pytest.raises(TypeError), id="complex"),
    pytest.param([5020], pytest.raises(TypeError), id="list[int]"),
    pytest.param({"seconds": 5020}, pytest.raises(TypeError), id="dict[str, int]"),
    pytest.param((datetime(2016, 1, 1),), pytest.raises(TypeError), id="tuple[datetime]"),
]


test_cases_valid = [
    # value, expected_result
    pytest.param(None, None, id="none"),
    pytest.param("", None, id="from_str_empty"),
    pytest.param("2016-01-06 01:23:40", datetime(2016, 1, 6, 1, 23, 40, tzinfo=None), id="from_str_1"),
    pytest.param("2016-01-06T01:23:40", datetime(2016, 1, 6, 1, 23, 40, tzinfo=None), id="from_str_2"),
    pytest.param("2016-01-06T01:23:40Z", datetime(2016, 1, 6, 1, 23, 40, tzinfo=timezone.utc), id="from_str_3"),
    pytest.param(5020, datetime(2016, 1, 6, 1, 23, 40, tzinfo=timezone.utc), id="from_int"),
    pytest.param(datetime(2016, 1, 6, 1, 23, 40), datetime(2016, 1, 6, 1, 23, 40, tzinfo=None), id="from_datetime_1"),
    pytest.param(datetime(2016, 1, 6, 1, 23, 40, tzinfo=None), datetime(2016, 1, 6, 1, 23, 40, tzinfo=None), id="from_datetime_2"),
    pytest.param(datetime(2016, 1, 6, 1, 23, 40, tzinfo=timezone.utc), datetime(2016, 1, 6, 1, 23, 40, tzinfo=timezone.utc), id="from_datetime_3"),
]


@pytest.mark.parametrize(["value", "expected_exception"], test_cases_invalid)
def test_parse_datetime_invalid(value: Any, expected_exception: AbstractContextManager):
    with expected_exception:
        _ = parse_datetime(value)


@pytest.mark.parametrize(["value", "expected_result"], test_cases_valid)
def test_parse_datetime_valid(value: Optional[Union[datetime, int, str]], expected_result: Optional[datetime]):
    result = parse_datetime(value)
    assert result == expected_result
