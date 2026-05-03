import datetime

import pytest

from src.api import utils
from src.api.database.crud import _get_date_defaults


test_cases__get_date_defaults = [
    # from_date, to_date, expected_from_date, expected_to_date
    pytest.param(
        None,
        None,
        datetime.datetime(2016, 1, 6),
        None,
        id="from_none_to_none",
    ),
    pytest.param(
        datetime.datetime(2018, 1, 6),
        None,
        datetime.datetime(2018, 1, 6),
        None,
        id="from_has_value_without_timezone_to_none",
    ),
    pytest.param(
        datetime.datetime(2018, 1, 6, tzinfo=datetime.timezone.utc),
        None,
        datetime.datetime(2018, 1, 6),
        None,
        id="from_has_value_with_timezone_to_none",
    ),
    pytest.param(
        None,
        datetime.datetime(2019, 1, 1),
        datetime.datetime(2016, 1, 6),
        datetime.datetime(2019, 1, 1),
        id="from_none_to_has_value_without_timezone",
    ),
    pytest.param(
        None,
        datetime.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2016, 1, 6),
        datetime.datetime(2019, 1, 1),
        id="from_none_to_has_value_with_timezone",
    ),
    pytest.param(
        datetime.datetime(2018, 1, 6),
        datetime.datetime(2019, 1, 1),
        datetime.datetime(2018, 1, 6),
        datetime.datetime(2019, 1, 1),
        id="from_has_value_without_timezone_to_has_value_without_timezone",
    ),
    pytest.param(
        datetime.datetime(2018, 1, 6),
        datetime.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2018, 1, 6),
        datetime.datetime(2019, 1, 1),
        id="from_has_value_without_timezone_to_has_value_with_timezone",
    ),
    pytest.param(
        datetime.datetime(2018, 1, 6, tzinfo=datetime.timezone.utc),
        datetime.datetime(2019, 1, 1),
        datetime.datetime(2018, 1, 6),
        datetime.datetime(2019, 1, 1),
        id="from_has_value_with_timezone_to_has_value_without_timezone",
    ),
    pytest.param(
        datetime.datetime(2018, 1, 6, tzinfo=datetime.timezone.utc),
        datetime.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2018, 1, 6),
        datetime.datetime(2019, 1, 1),
        id="from_has_value_with_timezone_to_has_value_with_timezone",
    ),
]
"""from_date, to_date, expected_from_date, expected_to_date"""


@pytest.mark.parametrize(["from_date", "to_date", "expected_from_date", "expected_to_date"], test_cases__get_date_defaults)
def test__get_date_defaults(
    from_date: datetime.datetime | None,
    to_date: datetime.datetime | None,
    expected_from_date: datetime.datetime,
    expected_to_date: datetime.datetime | None,
):
    utc_start = utils.remove_timezone(datetime.datetime.now(datetime.timezone.utc))

    from_date_result, to_date_result = _get_date_defaults(from_date, to_date)

    utc_end = utils.remove_timezone(datetime.datetime.now(datetime.timezone.utc))

    assert from_date_result == expected_from_date
    assert from_date_result.tzinfo is None

    if expected_to_date is None:
        assert to_date_result > utc_start and to_date_result < utc_end
    else:
        assert to_date_result == expected_to_date
