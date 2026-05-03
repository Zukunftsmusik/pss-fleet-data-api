import datetime as dt

import pytest
import test_cases_db
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_collections
from src.api.database.models import CollectionDB
from src.api.models.enums import ParameterInterval, ParameterOnMissing


test_cases_interval = [
    # interval, expected_length
    pytest.param(ParameterInterval.HOURLY, 37, id="by_interval hourly"),
    pytest.param(ParameterInterval.DAILY, 17, id="by_interval daily"),
    pytest.param(ParameterInterval.MONTHLY, 7, id="by_interval monthly"),
]

test_cases_by_date = [
    # from_date, to_date, expected_length
    pytest.param(None, None, 37, id="by_date None"),
    pytest.param(dt.datetime(2024, 4, 1), None, 35, id="by_date from_April_1st"),
    pytest.param(dt.datetime(2024, 4, 2), None, 33, id="by_date from_April_2nd"),
    pytest.param(None, dt.datetime(2024, 6, 1), 14, id="by_date to_June_1st"),
    pytest.param(dt.datetime(2024, 4, 1), dt.datetime(2024, 6, 1), 12, id="from_April_1st_to_June_1st"),
    pytest.param(dt.datetime(2024, 4, 2), dt.datetime(2024, 6, 1), 10, id="from_April_2nd_to_June_1st"),
]

test_cases_skip_take = [
    # skip, take, expected_length
    pytest.param(0, 100, 37, id="skip_0_take_100"),
    pytest.param(0, 18, 18, id="skip_0_take_18"),
    pytest.param(5, 18, 18, id="skip_5_take_18"),
    pytest.param(5, 13, 13, id="skip_5_take_13"),
    pytest.param(5, 5, 5, id="skip_5_take_5"),
    pytest.param(37, 100, 0, id="skip_18_take_100"),
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
async def test_get_collections_by_date(from_date: dt.datetime, to_date: dt.datetime, expected_length: int, session: AsyncSession):
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


@pytest.mark.parametrize(["interval", "to_date", "expected_timestamps", "expected_count"], test_cases_db.test_cases_parameter_onMissing_not_specified)
async def test_get_collections_onMissing_not_specified(
    interval: ParameterInterval, to_date: dt.datetime, expected_timestamps: list[dt.datetime | None], expected_count: int, session: AsyncSession
):
    collections = await get_collections(
        session,
        to_date=to_date,
        interval=interval,
        skip=0,
        take=3,
        desc=True,
    )

    assert len(collections) == expected_count
    for i in range(expected_count):
        assert collections[i].collected_at == expected_timestamps[i]


@pytest.mark.parametrize(["interval", "to_date", "expected_timestamps", "expected_count"], test_cases_db.test_cases_parameter_onMissing_not_specified)
async def test_get_collections_onMissing_skip(
    interval: ParameterInterval, to_date: dt.datetime, expected_timestamps: list[dt.datetime | None], expected_count: int, session: AsyncSession
):
    collections = await get_collections(
        session,
        to_date=to_date,
        interval=interval,
        skip=0,
        take=3,
        desc=True,
        on_missing=ParameterOnMissing.SKIP,
    )

    assert len(collections) == expected_count
    for i in range(expected_count):
        assert collections[i].collected_at == expected_timestamps[i]


@pytest.mark.parametrize(
    ["interval", "from_date", "to_date", "expected_timestamps", "expected_count"], test_cases_db.test_cases_parameter_onMissing_last_desc
)
async def test_get_collections_onMissing_last_desc(
    interval: ParameterInterval,
    from_date: dt.datetime,
    to_date: dt.datetime,
    expected_timestamps: list[dt.datetime | None],
    expected_count: int,
    session: AsyncSession,
):
    collections = await get_collections(
        session,
        from_date=from_date,
        to_date=to_date,
        interval=interval,
        skip=0,
        take=3,
        desc=True,
        on_missing=ParameterOnMissing.LAST,
    )

    assert len(collections) == expected_count
    for i in range(expected_count):
        assert collections[i].collected_at == expected_timestamps[i]


@pytest.mark.parametrize(
    ["interval", "from_date", "to_date", "expected_timestamps", "expected_count"], test_cases_db.test_cases_parameter_onMissing_last_asc
)
async def test_get_collections_onMissing_last_asc(
    interval: ParameterInterval,
    from_date: dt.datetime,
    to_date: dt.datetime,
    expected_timestamps: list[dt.datetime | None],
    expected_count: int,
    session: AsyncSession,
):
    collections = await get_collections(
        session,
        from_date=from_date,
        to_date=to_date,
        interval=interval,
        skip=0,
        take=3,
        desc=False,
        on_missing=ParameterOnMissing.LAST,
    )

    assert len(collections) == expected_count
    for i in range(expected_count):
        assert collections[i].collected_at == expected_timestamps[i]


@pytest.mark.parametrize(["interval", "to_date", "expected_timestamps", "expected_count"], test_cases_db.test_cases_parameter_onMissing_null)
async def test_get_collections_onMissing_null(
    interval: ParameterInterval, to_date: dt.datetime, expected_timestamps: list[dt.datetime | None], expected_count: int, session: AsyncSession
):
    collections = await get_collections(
        session,
        to_date=to_date,
        interval=interval,
        skip=0,
        take=3,
        desc=True,
        on_missing=ParameterOnMissing.NULL,
    )

    assert len(collections) == expected_count
    for i in range(expected_count):
        if expected_timestamps[i] is None:
            assert collections[i] is None
        else:
            assert collections[i].collected_at == expected_timestamps[i]


@pytest.mark.parametrize(
    ["interval", "to_date", "expected_timestamps", "expected_count", "empty_collection_index"], test_cases_db.test_cases_parameter_onMissing_empty
)
async def test_get_collections_onMissing_empty(
    interval: ParameterInterval,
    to_date: dt.datetime,
    expected_timestamps: list[dt.datetime | None],
    expected_count: int,
    empty_collection_index: int,
    session: AsyncSession,
):
    collections = await get_collections(
        session,
        to_date=to_date,
        interval=interval,
        skip=0,
        take=3,
        desc=True,
        on_missing=ParameterOnMissing.EMPTY,
    )

    assert len(collections) == expected_count
    for i in range(expected_count):
        assert collections[i].collected_at == expected_timestamps[i]

    __assert_dummy_collection(collections[empty_collection_index])


# ----- Helpers -----


def __assert_dummy_collection(collection: CollectionDB):
    assert collection.fleet_count == 0
    assert collection.user_count == 0
