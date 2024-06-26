from contextlib import AbstractContextManager
from contextlib import nullcontext as no_exception
from datetime import datetime
from typing import Sequence

import pytest
from sqlmodel import Session

from src.api.database.crud import get_alliance_history
from src.api.database.models import AllianceDB, CollectionDB
from src.api.models.enums import ParameterInterval

testcases_interval = [
    pytest.param(201549, ParameterInterval.HOURLY, 18, no_exception(), id="CRUD get_alliance_history by_interval hourly"),
    pytest.param(201549, ParameterInterval.DAILY, 9, no_exception(), id="CRUD get_alliance_history by_interval daily"),
    pytest.param(201549, ParameterInterval.MONTHLY, 3, no_exception(), id="CRUD get_alliance_history by_interval monthly"),
]

testcases_by_date = [
    pytest.param(201549, None, None, 18, no_exception(), id="CRUD get_alliance_history by_date None"),
    pytest.param(201549, datetime(2024, 4, 1), None, 16, no_exception(), id="CRUD get_alliance_history by_date from_April_1st"),
    pytest.param(201549, datetime(2024, 4, 2), None, 14, no_exception(), id="CRUD get_alliance_history by_date from_April_2nd"),
    pytest.param(201549, None, datetime(2024, 6, 1), 14, no_exception(), id="CRUD get_alliance_history by_date to_June_1st"),
    pytest.param(201549, datetime(2024, 4, 1), datetime(2024, 6, 1), 12, no_exception(), id="CRUD get_alliance_history from_April_1st_to_June_1st"),
    pytest.param(201549, datetime(2024, 4, 2), datetime(2024, 6, 1), 10, no_exception(), id="CRUD get_alliance_history from_April_2nd_to_June_1st"),
]

testcases_skip_take = [
    pytest.param(201549, 0, 100, 18, no_exception(), id="CRUD get_alliance_history skip_0_take_100"),
    pytest.param(201549, 0, 18, 18, no_exception(), id="CRUD get_alliance_history skip_0_take_18"),
    pytest.param(201549, 5, 18, 13, no_exception(), id="CRUD get_alliance_history skip_5_take_18"),
    pytest.param(201549, 5, 13, 13, no_exception(), id="CRUD get_alliance_history skip_5_take_13"),
    pytest.param(201549, 5, 5, 5, no_exception(), id="CRUD get_alliance_history skip_5_take_5"),
    pytest.param(201549, 18, 100, 0, no_exception(), id="CRUD get_alliance_history skip_18_take_100"),
    pytest.param(201549, 0, 0, 0, no_exception(), id="CRUD get_alliance_history skip_0_take_0"),
]

testcases_ordered_by = [
    pytest.param(201549, True, id="CRUD get_alliance_history ordered_asc"),
    pytest.param(201549, False, id="CRUD get_alliance_history ordered_desc"),
    pytest.param(201549, None, id="CRUD get_alliance_history ordered_None"),
]

testcases_include_users = [
    pytest.param(201549, True, id="CRUD get_alliance_history include_users_1"),
    pytest.param(201549, False, id="CRUD get_alliance_history include_users_2"),
]


@pytest.mark.parametrize("alliance_id,interval,expected_length,expected_exception", testcases_interval)
def test_get_alliance_history_by_interval(alliance_id: int, interval: ParameterInterval, expected_length: int, expected_exception: AbstractContextManager, session: Session):
    with expected_exception:
        alliance_history = get_alliance_history(session, alliance_id, False, None, None, interval, False, 0, 100)
        __assert_correct_types(alliance_history)
        assert len(alliance_history) == expected_length


@pytest.mark.parametrize("alliance_id,from_date,to_date,expected_length,expected_exception", testcases_by_date)
def test_get_alliance_history_by_date(alliance_id: int, from_date: datetime, to_date: datetime, expected_length: int, expected_exception: AbstractContextManager, session: Session):
    with expected_exception:
        alliance_history = get_alliance_history(session, alliance_id, False, from_date, to_date, ParameterInterval.HOURLY, False, 0, 100)
        __assert_correct_types(alliance_history)
        assert len(alliance_history) == expected_length


@pytest.mark.parametrize("alliance_id,skip,take,expected_length,expected_exception", testcases_skip_take)
def test_get_alliance_history_by_skip_take(alliance_id: int, skip: int, take: int, expected_length: int, expected_exception: AbstractContextManager, session: Session):
    with expected_exception:
        alliance_history = get_alliance_history(session, alliance_id, False, None, None, ParameterInterval.HOURLY, False, skip, take)
        __assert_correct_types(alliance_history)
        assert len(alliance_history) == expected_length


@pytest.mark.parametrize("alliance_id,desc", testcases_ordered_by)
def test_get_alliance_history_ordered_asc(alliance_id: int, desc: bool, session: Session):
    alliance_history = get_alliance_history(session, alliance_id, False, None, None, ParameterInterval.HOURLY, desc, 0, 100)
    __assert_correct_types(alliance_history)
    for entry_1, entry_2 in zip(alliance_history, alliance_history[1:]):
        if desc:
            assert entry_1[0].collected_at > entry_2[0].collected_at
        else:
            assert entry_1[0].collected_at < entry_2[0].collected_at


@pytest.mark.parametrize("alliance_id,include_users", testcases_include_users)
def test_get_alliance_history_include_users(alliance_id: int, include_users: bool, session: Session):
    alliance_history = get_alliance_history(session, alliance_id, include_users, None, None, ParameterInterval.HOURLY, False, 0, 100)
    __assert_correct_types(alliance_history)
    for _, alliance in alliance_history:
        assert bool(alliance.users) is include_users


def __assert_correct_types(alliance_history: list[tuple[CollectionDB, AllianceDB]]):
    assert isinstance(alliance_history, Sequence)
    for entry in alliance_history:
        assert isinstance(entry, tuple)
        assert len(entry) == 2
        assert isinstance(entry[0], CollectionDB)
        assert isinstance(entry[1], AllianceDB)
