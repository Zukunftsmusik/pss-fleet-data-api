from datetime import datetime

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_collections
from src.api.database.models import CollectionDB
from src.api.models.enums import ParameterInterval


test_cases_interval = [
    # interval, expected_length
    pytest.param(ParameterInterval.HOURLY, 18, id="by_interval hourly"),
    pytest.param(ParameterInterval.DAILY, 9, id="by_interval daily"),
    pytest.param(ParameterInterval.MONTHLY, 3, id="by_interval monthly"),
]

test_cases_by_date = [
    # from_date, to_date, expected_length
    pytest.param(None, None, 18, id="by_date None"),
    pytest.param(datetime(2024, 4, 1), None, 16, id="by_date from_April_1st"),
    pytest.param(datetime(2024, 4, 2), None, 14, id="by_date from_April_2nd"),
    pytest.param(None, datetime(2024, 6, 1), 14, id="by_date to_June_1st"),
    pytest.param(datetime(2024, 4, 1), datetime(2024, 6, 1), 12, id="from_April_1st_to_June_1st"),
    pytest.param(datetime(2024, 4, 2), datetime(2024, 6, 1), 10, id="from_April_2nd_to_June_1st"),
]

test_cases_skip_take = [
    # skip, take, expected_length
    pytest.param(0, 100, 18, id="skip_0_take_100"),
    pytest.param(0, 18, 18, id="skip_0_take_18"),
    pytest.param(5, 18, 13, id="skip_5_take_18"),
    pytest.param(5, 13, 13, id="skip_5_take_13"),
    pytest.param(5, 5, 5, id="skip_5_take_5"),
    pytest.param(18, 100, 0, id="skip_18_take_100"),
    pytest.param(0, 0, 0, id="skip_0_take_0"),
]

test_cases_ordered_by = [
    # desc
    pytest.param(True, id="ordered asc"),
    pytest.param(False, id="ordered desc"),
    pytest.param(None, id="ordered None"),
]


@pytest.mark.parametrize(["interval", "expected_length"], test_cases_interval)
async def test_get_collections_by_interval(interval: ParameterInterval, expected_length: int, session: AsyncSession):
    collections = await get_collections(session, interval=interval)
    assert all(isinstance(collection, CollectionDB) for collection in collections)
    assert len(collections) == expected_length


@pytest.mark.parametrize(["from_date", "to_date", "expected_length"], test_cases_by_date)
async def test_get_collections_by_date(from_date: datetime, to_date: datetime, expected_length: int, session: AsyncSession):
    collections = await get_collections(session, from_date=from_date, to_date=to_date, interval=ParameterInterval.HOURLY)
    assert all(isinstance(collection, CollectionDB) for collection in collections)
    assert len(collections) == expected_length


@pytest.mark.parametrize(["skip", "take", "expected_length"], test_cases_skip_take)
async def test_get_collections_by_skip_take(skip: int, take: int, expected_length: int, session: AsyncSession):
    collections = await get_collections(session, interval=ParameterInterval.HOURLY, skip=skip, take=take)
    assert all(isinstance(collection, CollectionDB) for collection in collections)
    assert len(collections) == expected_length


@pytest.mark.parametrize(["desc"], test_cases_ordered_by)
async def test_get_collections_ordered_asc(desc: bool, session: AsyncSession):
    collections = await get_collections(session, interval=ParameterInterval.HOURLY, desc=desc)
    assert all(isinstance(collection, CollectionDB) for collection in collections)
    for collection_1, collection_2 in zip(collections[:-1], collections[1:], strict=True):
        if desc:
            assert collection_1.collected_at > collection_2.collected_at
        else:
            assert collection_1.collected_at < collection_2.collected_at
