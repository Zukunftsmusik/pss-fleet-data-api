from datetime import datetime, timezone

import pytest

from src.api.models.exceptions import FromDateAfterToDateError
from src.api.routers import dependencies


test_cases_invalid = [
    # from_date, to_date, expected_exception
    pytest.param(
        datetime(2020, 1, 31, 23, 59),
        datetime(2020, 1, 1, 23, 59),
        pytest.raises(FromDateAfterToDateError),
        id="from_date_after_to_date",
    ),
]

test_cases_valid = [
    # from_date, to_date, expected_from_date, expected_to_date
    pytest.param(
        None,
        None,
        None,
        None,
        id="none",
    ),
    pytest.param(
        datetime(2020, 1, 1, 23, 59),
        None,
        datetime(2020, 1, 1, 23, 59),
        None,
        id="only_from_date",
    ),
    pytest.param(
        datetime(2020, 1, 1, 23, 59, tzinfo=timezone.utc),
        None,
        datetime(2020, 1, 1, 23, 59),
        None,
        id="only_from_date_utc",
    ),
    pytest.param(
        None,
        datetime(2020, 1, 1, 23, 59),
        None,
        datetime(2020, 1, 1, 23, 59),
        id="only_to_date",
    ),
    pytest.param(
        None,
        datetime(2020, 1, 1, 23, 59, tzinfo=timezone.utc),
        None,
        datetime(2020, 1, 1, 23, 59),
        id="only_to_date_utc",
    ),
    pytest.param(
        datetime(2020, 1, 1, 23, 59),
        datetime(2020, 1, 31, 23, 59),
        datetime(2020, 1, 1, 23, 59),
        datetime(2020, 1, 31, 23, 59),
        id="from_and_to_date",
    ),
    pytest.param(
        datetime(2020, 1, 1, 23, 59, tzinfo=timezone.utc),
        datetime(2020, 1, 31, 23, 59),
        datetime(2020, 1, 1, 23, 59),
        datetime(2020, 1, 31, 23, 59),
        id="from_and_to_date_from_utc",
    ),
    pytest.param(
        datetime(2020, 1, 1, 23, 59),
        datetime(2020, 1, 31, 23, 59, tzinfo=timezone.utc),
        datetime(2020, 1, 1, 23, 59),
        datetime(2020, 1, 31, 23, 59),
        id="from_and_to_date_to_utc",
    ),
    pytest.param(
        datetime(2020, 1, 1, 23, 59, tzinfo=timezone.utc),
        datetime(2020, 1, 31, 23, 59, tzinfo=timezone.utc),
        datetime(2020, 1, 1, 23, 59),
        datetime(2020, 1, 31, 23, 59),
        id="from_and_to_date_utc",
    ),
    pytest.param(
        datetime(2020, 1, 1, 23, 59, 0, 500),
        None,
        datetime(2020, 1, 1, 23, 59),
        None,
        id="remove_microseconds",
    ),
]


@pytest.mark.parametrize(["from_date", "to_date", "expected_exception"], test_cases_invalid)
async def test_from_to_date_parameters_from_before_to(from_date, to_date, expected_exception):
    with expected_exception:
        _ = await dependencies.from_to_date_parameters(from_date=from_date, to_date=to_date)


@pytest.mark.parametrize(["from_date", "to_date", "expected_from_date", "expected_to_date"], test_cases_valid)
async def test_from_to_date_parameters_valid(from_date: datetime, to_date: datetime, expected_from_date: datetime, expected_to_date: datetime):
    datetime_filter = await dependencies.from_to_date_parameters(from_date=from_date, to_date=to_date)
    assert datetime_filter.from_date == expected_from_date
    assert datetime_filter.to_date == expected_to_date
