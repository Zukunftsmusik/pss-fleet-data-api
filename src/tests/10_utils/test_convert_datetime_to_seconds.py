from datetime import datetime

import pytest
from dateutil.parser import parse as parse_datetime

from src.api.utils import convert_datetime_to_seconds


test_cases_invalid = [
    # value, expected_exception
    pytest.param(True, pytest.raises(TypeError), id="bool"),
    pytest.param(12.34, pytest.raises(TypeError), id="float"),
    pytest.param(1234, pytest.raises(TypeError), id="int"),
    pytest.param("1234", pytest.raises(TypeError), id="str"),
    pytest.param(complex("-1.23+4.5j"), pytest.raises(TypeError), id="complex"),
    pytest.param([5020], pytest.raises(TypeError), id="list[int]"),
    pytest.param({"seconds": 5020}, pytest.raises(TypeError), id="dict[str, int]"),
    pytest.param((datetime(2016, 1, 1),), pytest.raises(TypeError), id="tuple[datetime]"),
]


test_cases_valid = [
    # value, expected_result
    pytest.param(None, None, id="none"),
    pytest.param(parse_datetime("2016-01-07T01:23:40"), 91420, id="no_timezone"),
    pytest.param(parse_datetime("2016-01-07T01:23:40Z"), 91420, id="timezone_utc"),
    pytest.param(parse_datetime("2016-01-07T01:23:40+02:00"), 84220, id="timezone_mest"),
]


@pytest.mark.parametrize(["value", "expected_exception"], test_cases_invalid)
def test_convert_datetime_to_seconds_invalid(value, expected_exception):
    with expected_exception:
        _ = convert_datetime_to_seconds(value)


@pytest.mark.parametrize(["value", "expected_result"], test_cases_valid)
def test_convert_datetime_to_seconds_valid(value, expected_result):
    result = convert_datetime_to_seconds(value)
    assert result == expected_result
