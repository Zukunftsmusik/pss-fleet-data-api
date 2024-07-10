from datetime import datetime

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_collection_by_timestamp
from src.api.database.models import CollectionDB


test_cases_not_existing = [
    # timestamp
    pytest.param(datetime(1, 1, 1, 1, 1, 1), id="non_existing_timestamp"),
]


test_cases_existing = [
    # timestamp
    pytest.param(datetime(2024, 3, 31, 12, 59, 0), id="existing_timestamp"),
]


@pytest.mark.parametrize(["collection_id"], test_cases_not_existing)
async def test_get_collection_by_timestamp_invalid_timestamp(collection_id: int, session: AsyncSession):
    collection = await get_collection_by_timestamp(session, collection_id)
    assert collection is None


@pytest.mark.parametrize(["collection_id"], test_cases_existing)
async def test_get_collection_by_timestamp_valid_timestamp(collection_id: int, session: AsyncSession):
    collection = await get_collection_by_timestamp(session, collection_id)
    assert collection
    assert isinstance(collection, CollectionDB)
