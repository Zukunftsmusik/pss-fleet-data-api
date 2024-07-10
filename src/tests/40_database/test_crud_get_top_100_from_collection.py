import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_top_100_from_collection
from src.api.database.models import UserDB


test_cases_invalid = [
    # collection_id, skip, take, expected_length
    pytest.param(9001, 0, 100, 0, id="invalid_ID_1"),
    pytest.param(9001, 18, 100, 0, id="invalid_ID_2"),
    pytest.param(9001, 18, 82, 0, id="invalid_ID_3"),
    pytest.param(9001, 18, 7, 0, id="invalid_ID_4"),
]


test_cases_valid = [
    # collection_id, skip, take, expected_length
    pytest.param(1, 0, 100, 30, id="valid_ID_1"),
    pytest.param(1, 18, 100, 12, id="valid_ID_2"),
    pytest.param(1, 18, 82, 12, id="valid_ID_3"),
    pytest.param(1, 18, 7, 7, id="valid_ID_4"),
]


@pytest.mark.parametrize(["collection_id", "skip", "take", "expected_length"], test_cases_invalid)
async def test_get_top_100_from_collection_invalid(collection_id: int, skip: int, take: int, expected_length: int, session: AsyncSession):
    top_100 = await get_top_100_from_collection(session, collection_id, skip, take)
    assert isinstance(top_100, list)
    assert len(top_100) == expected_length
    if expected_length:
        assert all(isinstance(user, UserDB) for user in top_100)
        assert not any(user.alliance for user in top_100)
        for user_1, user_2 in zip(top_100[:-1], top_100[1:], strict=True):
            assert user_1.trophy >= user_2.trophy


@pytest.mark.parametrize(["collection_id", "skip", "take", "expected_length"], test_cases_valid)
async def test_get_top_100_from_collection_valid(collection_id: int, skip: int, take: int, expected_length: int, session: AsyncSession):
    top_100 = await get_top_100_from_collection(session, collection_id, skip, take)
    assert isinstance(top_100, list)
    assert len(top_100) == expected_length
    assert all(isinstance(user, UserDB) for user in top_100)
    assert not any(user.alliance for user in top_100)
    for user_1, user_2 in zip(top_100[:-1], top_100[1:], strict=True):
        assert user_1.trophy >= user_2.trophy
