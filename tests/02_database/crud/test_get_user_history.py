from contextlib import AbstractContextManager
from contextlib import nullcontext as no_exception
from datetime import datetime
from typing import Sequence

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_user_history
from src.api.database.models import CollectionDB, UserDB
from src.api.models.enums import ParameterInterval

testcases_interval = [
    pytest.param(20013541, ParameterInterval.HOURLY, 18, no_exception(), id="CRUD get_user_history by_interval hourly"),
    pytest.param(20013541, ParameterInterval.DAILY, 9, no_exception(), id="CRUD get_user_history by_interval daily"),
    pytest.param(20013541, ParameterInterval.MONTHLY, 3, no_exception(), id="CRUD get_user_history by_interval monthly"),
]

testcases_by_date = [
    pytest.param(20013541, None, None, 18, no_exception(), id="CRUD get_user_history by_date None"),
    pytest.param(20013541, datetime(2024, 4, 1), None, 16, no_exception(), id="CRUD get_user_history by_date from_April_1st"),
    pytest.param(20013541, datetime(2024, 4, 2), None, 14, no_exception(), id="CRUD get_user_history by_date from_April_2nd"),
    pytest.param(20013541, None, datetime(2024, 6, 1), 14, no_exception(), id="CRUD get_user_history by_date to_June_1st"),
    pytest.param(20013541, datetime(2024, 4, 1), datetime(2024, 6, 1), 12, no_exception(), id="CRUD get_user_history from_April_1st_to_June_1st"),
    pytest.param(20013541, datetime(2024, 4, 2), datetime(2024, 6, 1), 10, no_exception(), id="CRUD get_user_history from_April_2nd_to_June_1st"),
]

testcases_skip_take = [
    pytest.param(20013541, 0, 100, 18, no_exception(), id="CRUD get_user_history skip_0_take_100"),
    pytest.param(20013541, 0, 18, 18, no_exception(), id="CRUD get_user_history skip_0_take_18"),
    pytest.param(20013541, 5, 18, 13, no_exception(), id="CRUD get_user_history skip_5_take_18"),
    pytest.param(20013541, 5, 13, 13, no_exception(), id="CRUD get_user_history skip_5_take_13"),
    pytest.param(20013541, 5, 5, 5, no_exception(), id="CRUD get_user_history skip_5_take_5"),
    pytest.param(20013541, 18, 100, 0, no_exception(), id="CRUD get_user_history skip_18_take_100"),
    pytest.param(20013541, 0, 0, 0, no_exception(), id="CRUD get_user_history skip_0_take_0"),
]

testcases_ordered_by = [
    pytest.param(20013541, True, id="CRUD get_user_history ordered_asc"),
    pytest.param(20013541, False, id="CRUD get_user_history ordered_desc"),
    pytest.param(20013541, None, id="CRUD get_user_history ordered_None"),
]

testcases_include_alliance = [
    pytest.param(20013541, True, id="CRUD get_user_history include_alliance_1"),
    pytest.param(20013541, False, id="CRUD get_user_history include_alliance_2"),
]


@pytest.mark.parametrize("user_id,interval,expected_length,expected_exception", testcases_interval)
async def test_get_user_history_by_interval(user_id: int, interval: ParameterInterval, expected_length: int, expected_exception: AbstractContextManager, session: AsyncSession):
    with expected_exception:
        user_history = await get_user_history(session, user_id, False, None, None, interval, False, 0, 100)
        __assert_correct_types(user_history)
        assert len(user_history) == expected_length


@pytest.mark.parametrize("user_id,from_date,to_date,expected_length,expected_exception", testcases_by_date)
async def test_get_user_history_by_date(user_id: int, from_date: datetime, to_date: datetime, expected_length: int, expected_exception: AbstractContextManager, session: AsyncSession):
    with expected_exception:
        user_history = await get_user_history(session, user_id, False, from_date, to_date, ParameterInterval.HOURLY, False, 0, 100)
        __assert_correct_types(user_history)
        assert len(user_history) == expected_length


@pytest.mark.parametrize("user_id,skip,take,expected_length,expected_exception", testcases_skip_take)
async def test_get_user_history_by_skip_take(user_id: int, skip: int, take: int, expected_length: int, expected_exception: AbstractContextManager, session: AsyncSession):
    with expected_exception:
        user_history = await get_user_history(session, user_id, False, None, None, ParameterInterval.HOURLY, False, skip, take)
        __assert_correct_types(user_history)
        assert len(user_history) == expected_length


@pytest.mark.parametrize("user_id,desc", testcases_ordered_by)
async def test_get_user_history_ordered_asc(user_id: int, desc: bool, session: AsyncSession):
    user_history = await get_user_history(session, user_id, False, None, None, ParameterInterval.HOURLY, desc, 0, 100)
    __assert_correct_types(user_history)
    for entry_1, entry_2 in zip(user_history, user_history[1:]):
        if desc:
            assert entry_1[0].collected_at > entry_2[0].collected_at
        else:
            assert entry_1[0].collected_at < entry_2[0].collected_at


@pytest.mark.parametrize("user_id,include_alliance", testcases_include_alliance)
async def test_get_user_history_include_alliance(user_id: int, include_alliance: bool, session: AsyncSession):
    user_history = await get_user_history(session, user_id, include_alliance, None, None, ParameterInterval.HOURLY, False, 0, 100)
    __assert_correct_types(user_history)
    for _, user in user_history:
        if user.alliance_id:
            assert bool(user.alliance) is include_alliance


def __assert_correct_types(user_history: list[tuple[CollectionDB, UserDB]]):
    assert isinstance(user_history, Sequence)
    for entry in user_history:
        assert isinstance(entry, tuple)
        assert len(entry) == 2
        assert isinstance(entry[0], CollectionDB)
        assert isinstance(entry[1], UserDB)
