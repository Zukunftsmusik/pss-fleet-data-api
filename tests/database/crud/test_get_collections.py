from contextlib import AbstractContextManager
from contextlib import nullcontext as no_exception
from datetime import datetime

import pytest
from sqlmodel import Session

from src.api.database.crud import get_collections
from src.api.database.models import CollectionDB
from src.api.models.enums import ParameterInterval

testcases_interval = [
    pytest.param(ParameterInterval.HOURLY, 18, no_exception(), id="CRUD get_collections by_interval hourly"),
    pytest.param(ParameterInterval.DAILY, 9, no_exception(), id="CRUD get_collections by_interval daily"),
    pytest.param(ParameterInterval.MONTHLY, 3, no_exception(), id="CRUD get_collections by_interval monthly"),
]

testcases_by_date = [
    pytest.param(None, None, 18, no_exception(), id="CRUD get_collections by_date None"),
    pytest.param(datetime(2024, 4, 1), None, 16, no_exception(), id="CRUD get_collections by_date from_April_1st"),
    pytest.param(datetime(2024, 4, 2), None, 14, no_exception(), id="CRUD get_collections by_date from_April_2nd"),
    pytest.param(None, datetime(2024, 6, 1), 14, no_exception(), id="CRUD get_collections by_date to_June_1st"),
    pytest.param(datetime(2024, 4, 1), datetime(2024, 6, 1), 12, no_exception(), id="CRUD get_collections from_April_1st_to_June_1st"),
    pytest.param(datetime(2024, 4, 2), datetime(2024, 6, 1), 10, no_exception(), id="CRUD get_collections from_April_2nd_to_June_1st"),
]

testcases_skip_take = [
    pytest.param(0, 100, 18, no_exception(), id="CRUD get_collections skip_0_take_100"),
    pytest.param(0, 18, 18, no_exception(), id="CRUD get_collections skip_0_take_18"),
    pytest.param(5, 18, 13, no_exception(), id="CRUD get_collections skip_5_take_18"),
    pytest.param(5, 13, 13, no_exception(), id="CRUD get_collections skip_5_take_13"),
    pytest.param(5, 5, 5, no_exception(), id="CRUD get_collections skip_5_take_5"),
    pytest.param(18, 100, 0, no_exception(), id="CRUD get_collections skip_18_take_100"),
    pytest.param(0, 0, 0, no_exception(), id="CRUD get_collections skip_0_take_0"),
]

testcases_ordered_by = [
    pytest.param(True, id="CRUD get_collections ordered asc"),
    pytest.param(False, id="CRUD get_collections ordered desc"),
    pytest.param(None, id="CRUD get_collections ordered None"),
]


@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("interval,expected_length,expected_exception", testcases_interval)
def test_get_collections_by_interval(interval: ParameterInterval, expected_length: int, expected_exception: AbstractContextManager, session: Session):
    with expected_exception:
        collections = get_collections(session, None, None, interval, False, 0, 100)
        assert all(isinstance(collection, CollectionDB) for collection in collections)
        assert len(collections) == expected_length


@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("from_date,to_date,expected_length,expected_exception", testcases_by_date)
def test_get_collections_by_date(from_date: datetime, to_date: datetime, expected_length: int, expected_exception: AbstractContextManager, session: Session):
    with expected_exception:
        collections = get_collections(session, from_date, to_date, ParameterInterval.HOURLY, False, 0, 100)
        assert all(isinstance(collection, CollectionDB) for collection in collections)
        assert len(collections) == expected_length


@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("skip,take,expected_length,expected_exception", testcases_skip_take)
def test_get_collections_by_skip_take(skip: int, take: int, expected_length: int, expected_exception: AbstractContextManager, session: Session):
    with expected_exception:
        collections = get_collections(session, None, None, ParameterInterval.HOURLY, False, skip, take)
        assert all(isinstance(collection, CollectionDB) for collection in collections)
        assert len(collections) == expected_length


@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("desc", testcases_ordered_by)
def test_get_collections_ordered_asc(desc: bool, session: Session):
    collections = get_collections(session, None, None, ParameterInterval.HOURLY, desc, 0, 100)
    assert all(isinstance(collection, CollectionDB) for collection in collections)
    for collection_1, collection_2 in zip(collections, collections[1:]):
        if desc:
            assert collection_1.collected_at > collection_2.collected_at
        else:
            assert collection_1.collected_at < collection_2.collected_at
