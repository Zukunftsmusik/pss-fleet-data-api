import datetime as dt

import pytest

from src.api.models.enums import ParameterInterval


test_cases_parameter_onMissing_not_specified = [
    # interval, to_date, expected_timestamps, expected_count
    pytest.param(
        ParameterInterval.HOURLY,
        dt.datetime(2025, 9, 30, 20, 0, 0),
        [
            dt.datetime(2025, 9, 30, 19, 59, 0),
            dt.datetime(2025, 9, 30, 18, 59, 0),
            # this one is missing in the test data
            dt.datetime(2025, 9, 30, 16, 59, 0),
        ],
        3,
        id="interval_hourly",
    ),
    pytest.param(
        ParameterInterval.DAILY,
        dt.datetime(2025, 9, 29, 0, 0, 0),
        [
            dt.datetime(2025, 9, 28, 23, 59, 0),
            dt.datetime(2025, 9, 27, 23, 59, 0),
            # this one is missing in the test data
            dt.datetime(2025, 9, 25, 23, 59, 0),
        ],
        3,
        id="interval_daily",
    ),
    pytest.param(
        ParameterInterval.MONTHLY,
        dt.datetime(2025, 10, 1, 0, 0, 0),
        [
            # this one is missing in the test data
            dt.datetime(2025, 8, 31, 23, 59, 0),
            dt.datetime(2025, 7, 31, 23, 59, 0),
            dt.datetime(2025, 6, 30, 23, 59, 0),
        ],
        3,
        id="interval_monthly",
    ),
]
"""interval, to_date, on_missing, expected_timestamps, expected_count"""

test_cases_parameter_onMissing_last_desc = [
    # interval, from_date, to_date, expected_timestamps, expected_count
    pytest.param(
        ParameterInterval.HOURLY,
        dt.datetime(2025, 9, 30, 16, 0, 0),
        dt.datetime(2025, 9, 30, 20, 0, 0),
        [
            dt.datetime(2025, 9, 30, 19, 59, 0),
            dt.datetime(2025, 9, 30, 18, 59, 0),
            # this one is missing in the test data
            dt.datetime(2025, 9, 30, 16, 59, 0),
        ],
        3,
        id="interval_hourly",
    ),
    pytest.param(
        ParameterInterval.DAILY,
        dt.datetime(2025, 9, 25, 0, 0, 0),
        dt.datetime(2025, 9, 29, 0, 0, 0),
        [
            dt.datetime(2025, 9, 28, 23, 59, 0),
            dt.datetime(2025, 9, 27, 23, 59, 0),
            # this one is missing in the test data
            dt.datetime(2025, 9, 26, 22, 59, 0),
        ],
        3,
        id="interval_daily",
    ),
    pytest.param(
        ParameterInterval.MONTHLY,
        dt.datetime(2025, 7, 1, 0, 0, 0),
        dt.datetime(2025, 11, 1, 0, 0, 0),
        [
            dt.datetime(2025, 10, 31, 23, 59, 0),
            # this one is missing in the test data
            dt.datetime(2025, 9, 30, 22, 59, 0),
            dt.datetime(2025, 8, 31, 23, 59, 0),
        ],
        3,
        id="interval_monthly",
    ),
]
"""interval, from_date, to_date, on_missing, expected_timestamps, expected_count"""

test_cases_parameter_onMissing_last_asc = [
    # interval, from_date, to_date, expected_timestamps, expected_count
    pytest.param(
        ParameterInterval.HOURLY,
        dt.datetime(2025, 9, 30, 16, 0, 0),
        dt.datetime(2025, 9, 30, 20, 0, 0),
        [
            dt.datetime(2025, 9, 30, 16, 59, 0),
            # this one is missing in the test data
            dt.datetime(2025, 9, 30, 18, 59, 0),
            dt.datetime(2025, 9, 30, 19, 59, 0),
        ],
        3,
        id="interval_hourly",
    ),
    pytest.param(
        ParameterInterval.DAILY,
        dt.datetime(2025, 9, 25, 0, 0, 0),
        dt.datetime(2025, 9, 29, 0, 0, 0),
        [
            dt.datetime(2025, 9, 25, 23, 59, 0),
            dt.datetime(2025, 9, 26, 22, 59, 0),
            # this one is missing in the test data
            dt.datetime(2025, 9, 27, 23, 59, 0),
        ],
        3,
        id="interval_daily",
    ),
    pytest.param(
        ParameterInterval.MONTHLY,
        dt.datetime(2025, 7, 1, 0, 0, 0),
        dt.datetime(2025, 11, 1, 0, 0, 0),
        [
            dt.datetime(2025, 7, 31, 23, 59, 0),
            dt.datetime(2025, 8, 31, 23, 59, 0),
            # this one is missing in the test data
            dt.datetime(2025, 9, 30, 22, 59, 0),
        ],
        3,
        id="interval_monthly",
    ),
]
"""interval, from_date, to_date, on_missing, expected_timestamps, expected_count"""

test_cases_parameter_onMissing_null = [
    # interval, to_date, expected_timestamps, expected_count
    pytest.param(
        ParameterInterval.HOURLY,
        dt.datetime(2025, 9, 30, 20, 0, 0),
        [
            dt.datetime(2025, 9, 30, 19, 59, 0),
            dt.datetime(2025, 9, 30, 18, 59, 0),
            None,  # 17:59 is missing in the test data
        ],
        3,
        id="interval_hourly",
    ),
    pytest.param(
        ParameterInterval.DAILY,
        dt.datetime(2025, 9, 29, 0, 0, 0),
        [
            dt.datetime(2025, 9, 28, 23, 59, 0),
            dt.datetime(2025, 9, 27, 23, 59, 0),
            None,  # this one is missing in the test data
        ],
        3,
        id="interval_daily",
    ),
    pytest.param(
        ParameterInterval.MONTHLY,
        dt.datetime(2025, 10, 1, 0, 0, 0),
        [
            None,  # this one is missing in the test data
            dt.datetime(2025, 8, 31, 23, 59, 0),
            dt.datetime(2025, 7, 31, 23, 59, 0),
        ],
        3,
        id="interval_monthly",
    ),
]
"""interval, to_date, on_missing, expected_timestamps, expected_count"""

test_cases_parameter_onMissing_empty = [
    # interval, to_date, expected_timestamps, expected_count, empty_collection_index
    pytest.param(
        ParameterInterval.HOURLY,
        dt.datetime(2025, 9, 30, 20, 0, 0),
        [
            dt.datetime(2025, 9, 30, 19, 59, 0),
            dt.datetime(2025, 9, 30, 18, 59, 0),
            dt.datetime(2025, 9, 30, 17, 59, 0),  # this one is missing in the test data
        ],
        3,
        2,
        id="interval_hourly",
    ),
    pytest.param(
        ParameterInterval.DAILY,
        dt.datetime(2025, 9, 29, 0, 0, 0),
        [
            dt.datetime(2025, 9, 28, 23, 59, 0),
            dt.datetime(2025, 9, 27, 23, 59, 0),
            dt.datetime(2025, 9, 26, 23, 59, 0),  # this one is missing in the test data
        ],
        3,
        2,
        id="interval_daily",
    ),
    pytest.param(
        ParameterInterval.MONTHLY,
        dt.datetime(2025, 10, 1, 0, 0, 0),
        [
            dt.datetime(2025, 9, 30, 23, 59, 0),  # this one is missing in the test data
            dt.datetime(2025, 8, 31, 23, 59, 0),
            dt.datetime(2025, 7, 31, 23, 59, 0),
        ],
        3,
        0,
        id="interval_monthly",
    ),
]
"""interval, to_date, on_missing, expected_timestamps, expected_count, empty_collection_index"""


__all__ = [
    "test_cases_parameter_onMissing_not_specified",
    "test_cases_parameter_onMissing_last_desc",
    "test_cases_parameter_onMissing_null",
    "test_cases_parameter_onMissing_empty",
]
