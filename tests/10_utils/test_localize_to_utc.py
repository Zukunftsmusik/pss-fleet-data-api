from datetime import datetime, timezone

import pytest
from dateutil.parser import parse as parse_datetime

from src.api.utils import localize_to_utc


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
    pytest.param(parse_datetime("2016-01-06T01:23:40"), datetime(2016, 1, 6, 1, 23, 40, tzinfo=timezone.utc), id="no_timezone"),
    pytest.param(parse_datetime("2016-01-06T01:23:40Z"), datetime(2016, 1, 6, 1, 23, 40, tzinfo=timezone.utc), id="timezone_utc"),
    pytest.param(parse_datetime("2016-01-06T01:23:40+02:00"), datetime(2016, 1, 5, 23, 23, 40, tzinfo=timezone.utc), id="timezone_mest"),
]


@pytest.mark.parametrize(["value", "expected_exception"], test_cases_invalid)
def test_localize_to_utc_invalid(value, expected_exception):
    with expected_exception:
        _ = localize_to_utc(value)


@pytest.mark.parametrize(["value", "expected_result"], test_cases_valid)
def test_localize_to_utc_valid(value, expected_result):
    result = localize_to_utc(value)
    assert result == expected_result
