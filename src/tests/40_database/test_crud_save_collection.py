from contextlib import AbstractContextManager
from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_collection, save_collection
from src.api.database.models import CollectionDB


test_cases = [
    # include_alliances, include_users
    pytest.param(False, False, id="no_alliances_no_users"),
    pytest.param(True, False, id="with_alliances_no_users"),
    pytest.param(False, True, id="no_alliances_with_users"),
    pytest.param(True, True, id="with_alliances_with_users"),
]

test_cases_non_unique = [
    # override_id, override_timestamp, expected_exception
    pytest.param(1, None, pytest.raises(IntegrityError), id="non_unique collection_id"),
    pytest.param(None, datetime(2024, 4, 30, 23, 59), pytest.raises(IntegrityError), id="non_unique timestamp"),
]


@pytest.mark.usefixtures("new_collection")
@pytest.mark.parametrize(["include_alliances", "include_users"], test_cases)
async def test_save_collection(include_alliances: bool, include_users: bool, session: AsyncSession, new_collection: CollectionDB):
    collection = await save_collection(session, new_collection, include_alliances, include_users)
    collection_id = collection.collection_id
    assert collection_id is not None
    collection.collection_id = None
    assert dict(collection) == dict(new_collection)

    inserted_collection = await get_collection(session, collection_id, include_alliances, include_users)
    assert bool(inserted_collection.alliances) == include_alliances
    assert bool(inserted_collection.users) == include_users


@pytest.mark.usefixtures("new_collection")
@pytest.mark.parametrize(["override_id", "override_timestamp", "expected_exception"], test_cases_non_unique)
async def test_save_collection_non_unique(
    override_id: int, override_timestamp: datetime, expected_exception: AbstractContextManager, session: AsyncSession, new_collection: CollectionDB
):
    with expected_exception:
        if override_id is not None:
            new_collection.collection_id = override_id
        if override_timestamp:
            new_collection.collected_at = override_timestamp
        _ = await save_collection(session, new_collection, False, False)
