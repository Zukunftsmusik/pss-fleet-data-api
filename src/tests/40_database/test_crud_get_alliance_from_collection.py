from typing import Optional

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_alliance_from_collection
from src.api.database.models import AllianceDB, CollectionDB, UserDB


test_cases_invalid_ids = [
    # collection_id, alliance_id
    pytest.param(1, 1, id="invalid_alliance_id_1"),
    pytest.param(1, 1, id="invalid_alliance_id_2"),
    pytest.param(9001, 21, id="invalid_collection_id_1"),
    pytest.param(9001, 21, id="invalid_collection_id_2"),
    pytest.param(9001, 1, id="invalid_ids_1"),
    pytest.param(9001, 1, id="invalid_ids_2"),
]

test_cases_valid_ids = [
    # collection_id, alliance_id, expected_user_count
    pytest.param(1, 205164, 10, id="valid_ids_1"),
    pytest.param(8, 205164, 6, id="valid_ids_2"),
    pytest.param(8, 201549, 15, id="valid_ids_3"),
]


@pytest.mark.parametrize(["collection_id", "alliance_id"], test_cases_invalid_ids)
async def test_get_alliance_from_collection_invalid_ids(collection_id: int, alliance_id: int, session: AsyncSession):
    alliance_from_collection = await get_alliance_from_collection(session, collection_id, alliance_id)
    assert not alliance_from_collection


@pytest.mark.parametrize(["collection_id", "alliance_id", "expected_user_count"], test_cases_valid_ids)
async def test_get_alliance_from_collection_valid_ids(
    collection_id: int, alliance_id: int, expected_user_count: Optional[int], session: AsyncSession
):
    alliance_history = await get_alliance_from_collection(session, collection_id, alliance_id)
    assert alliance_history

    assert isinstance(alliance_history, tuple)
    assert len(alliance_history) == 2
    assert isinstance(alliance_history[0], CollectionDB)
    assert isinstance(alliance_history[1], AllianceDB)

    assert len(alliance_history[1].users) == expected_user_count
    if expected_user_count:
        assert all(isinstance(user, UserDB) for user in alliance_history[1].users)
