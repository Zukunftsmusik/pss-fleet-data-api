import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_collection
from src.api.database.models import AllianceDB, CollectionDB, UserDB


test_cases_invalid = [
    # collection_id, include_alliances, include_users
    pytest.param(9001, False, False, id="invalid_ID_1"),
    pytest.param(9001, True, False, id="invalid_ID_2"),
    pytest.param(9001, False, True, id="invalid_ID_3"),
    pytest.param(9001, True, True, id="invalid_ID_4"),
]


test_cases_valid = [
    # collection_id, include_alliances, include_users
    pytest.param(1, False, False, id="valid_ID_1"),
    pytest.param(1, True, False, id="valid_ID_2"),
    pytest.param(1, False, True, id="valid_ID_3"),
    pytest.param(1, True, True, id="valid_ID_4"),
]


@pytest.mark.parametrize(["collection_id", "include_alliances", "include_users"], test_cases_invalid)
async def test_get_collection_invalid_id(collection_id: int, include_alliances: bool, include_users: bool, session: AsyncSession):
    collection = await get_collection(session, collection_id, include_alliances, include_users)
    assert collection is None


@pytest.mark.parametrize(["collection_id", "include_alliances", "include_users"], test_cases_valid)
async def test_get_collection_valid_id(collection_id: int, include_alliances: bool, include_users: bool, session: AsyncSession):
    collection = await get_collection(session, collection_id, include_alliances, include_users)
    assert collection
    assert isinstance(collection, CollectionDB)
    if include_alliances:
        assert collection.alliances
        assert isinstance(collection.alliances[0], AllianceDB)
    if include_users:
        assert collection.users
        assert isinstance(collection.users[0], UserDB)
