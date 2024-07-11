import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_user_from_collection
from src.api.database.models import CollectionDB, UserDB


test_cases_invalid_ids = [
    # collection_id, user_id
    pytest.param(1, 1, id="invalid_user_id_1"),
    pytest.param(1, 1, id="invalid_user_id_2"),
    pytest.param(9001, 20013541, id="invalid_collection_id_1"),
    pytest.param(9001, 20013541, id="invalid_collection_id_2"),
    pytest.param(9001, 1, id="invalid_ids_1"),
    pytest.param(9001, 1, id="invalid_ids_2"),
]

test_cases_valid_ids = [
    # collection_id, user_id
    pytest.param(1, 20013541, id="valid_ids_1"),
    pytest.param(1, 20013541, id="valid_ids_2"),
    pytest.param(8, 20013541, id="valid_ids_3"),
    pytest.param(8, 20013541, id="valid_ids_4"),
]


@pytest.mark.parametrize(["collection_id", "user_id"], test_cases_invalid_ids)
async def test_get_user_from_collection_invalid_ids(collection_id: int, user_id: int, session: AsyncSession):
    user_history = await get_user_from_collection(session, collection_id, user_id)
    assert not user_history


@pytest.mark.parametrize(["collection_id", "user_id"], test_cases_valid_ids)
async def test_get_user_from_collection_valid_ids(collection_id: int, user_id: int, session: AsyncSession):
    user_history = await get_user_from_collection(session, collection_id, user_id)

    assert isinstance(user_history, tuple)
    assert len(user_history) == 2

    assert isinstance(user_history[0], CollectionDB)
    assert user_history[0].collection_id == collection_id

    assert isinstance(user_history[1], UserDB)
    assert user_history[1].collection_id == collection_id
    assert user_history[1].user_id == user_id
