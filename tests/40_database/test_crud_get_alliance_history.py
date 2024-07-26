from datetime import datetime
from typing import Sequence

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_alliance_history
from src.api.database.models import AllianceDB, CollectionDB
from src.api.models.enums import ParameterInterval


test_cases_interval = [
    # alliance_id, interval, expected_length
    pytest.param(201549, ParameterInterval.HOURLY, 18, id="by_interval hourly"),
    pytest.param(201549, ParameterInterval.DAILY, 9, id="by_interval daily"),
    pytest.param(201549, ParameterInterval.MONTHLY, 3, id="by_interval monthly"),
]

test_cases_by_date = [
    # alliance_id, from_date, to_date, expected_length
    pytest.param(201549, None, None, 18, id="by_date None"),
    pytest.param(201549, datetime(2024, 4, 1), None, 16, id="by_date from_April_1st"),
    pytest.param(201549, datetime(2024, 4, 2), None, 14, id="by_date from_April_2nd"),
    pytest.param(201549, None, datetime(2024, 6, 1), 14, id="by_date to_June_1st"),
    pytest.param(201549, datetime(2024, 4, 1), datetime(2024, 6, 1), 12, id="from_April_1st_to_June_1st"),
    pytest.param(201549, datetime(2024, 4, 2), datetime(2024, 6, 1), 10, id="from_April_2nd_to_June_1st"),
]

test_cases_skip_take = [
    # alliance_id, skip, take, expected_length
    pytest.param(201549, 0, 100, 18, id="skip_0_take_100"),
    pytest.param(201549, 0, 18, 18, id="skip_0_take_18"),
    pytest.param(201549, 5, 18, 13, id="skip_5_take_18"),
    pytest.param(201549, 5, 13, 13, id="skip_5_take_13"),
    pytest.param(201549, 5, 5, 5, id="skip_5_take_5"),
    pytest.param(201549, 18, 100, 0, id="skip_18_take_100"),
    pytest.param(201549, 0, 0, 0, id="skip_0_take_0"),
]

test_cases_ordered_by = [
    # alliance_id, desc
    pytest.param(201549, True, id="ordered_asc"),
    pytest.param(201549, False, id="ordered_desc"),
    pytest.param(201549, None, id="ordered_None"),
]

test_cases_include_users = [
    # alliance_id, include_users
    pytest.param(201549, True, id="include_users_1"),
    pytest.param(201549, False, id="include_users_2"),
]


@pytest.mark.parametrize(["alliance_id", "interval", "expected_length"], test_cases_interval)
async def test_get_alliance_history_by_interval(alliance_id: int, interval: ParameterInterval, expected_length: int, session: AsyncSession):
    alliance_history = await get_alliance_history(session, alliance_id, interval=interval)
    __assert_correct_types(alliance_history)
    assert len(alliance_history) == expected_length


@pytest.mark.parametrize(["alliance_id", "from_date", "to_date", "expected_length"], test_cases_by_date)
async def test_get_alliance_history_by_date(alliance_id: int, from_date: datetime, to_date: datetime, expected_length: int, session: AsyncSession):
    alliance_history = await get_alliance_history(session, alliance_id, from_date=from_date, to_date=to_date, interval=ParameterInterval.HOURLY)
    __assert_correct_types(alliance_history)
    assert len(alliance_history) == expected_length


@pytest.mark.parametrize(["alliance_id", "skip", "take", "expected_length"], test_cases_skip_take)
async def test_get_alliance_history_by_skip_take(alliance_id: int, skip: int, take: int, expected_length: int, session: AsyncSession):
    alliance_history = await get_alliance_history(session, alliance_id, interval=ParameterInterval.HOURLY, skip=skip, take=take)
    __assert_correct_types(alliance_history)
    assert len(alliance_history) == expected_length


@pytest.mark.parametrize(["alliance_id", "desc"], test_cases_ordered_by)
async def test_get_alliance_history_ordered_asc(alliance_id: int, desc: bool, session: AsyncSession):
    alliance_history = await get_alliance_history(session, alliance_id, interval=ParameterInterval.HOURLY, desc=desc)
    __assert_correct_types(alliance_history)
    for entry_1, entry_2 in zip(alliance_history[:-1], alliance_history[1:], strict=True):
        if desc:
            assert entry_1[0].collected_at > entry_2[0].collected_at
        else:
            assert entry_1[0].collected_at < entry_2[0].collected_at


def __assert_correct_types(alliance_history: list[tuple[CollectionDB, AllianceDB]]):
    assert isinstance(alliance_history, Sequence)
    for entry in alliance_history:
        assert isinstance(entry, tuple)
        assert len(entry) == 2
        assert isinstance(entry[0], CollectionDB)
        assert isinstance(entry[1], AllianceDB)
