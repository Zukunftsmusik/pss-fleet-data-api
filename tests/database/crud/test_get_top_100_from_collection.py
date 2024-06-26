from contextlib import AbstractContextManager
from contextlib import nullcontext as no_exception

import pytest
from sqlmodel import Session

from src.api.database.crud import get_top_100_from_collection
from src.api.database.models import UserDB

testcases = [
    pytest.param(1, 0, 100, 30, no_exception(), id="CRUD get_top_100_from_collection valid_ID_1"),
    pytest.param(1, 18, 100, 12, no_exception(), id="CRUD get_top_100_from_collections valid_ID_2"),
    pytest.param(1, 18, 82, 12, no_exception(), id="CRUD get_top_100_from_collections valid_ID_3"),
    pytest.param(1, 18, 7, 7, no_exception(), id="CRUD get_top_100_from_collections valid_ID_4"),
    pytest.param(9001, 0, 100, 0, no_exception(), id="CRUD get_top_100_from_collection valid_ID_1"),
    pytest.param(9001, 18, 100, 0, no_exception(), id="CRUD get_top_100_from_collections valid_ID_2"),
    pytest.param(9001, 18, 82, 0, no_exception(), id="CRUD get_top_100_from_collections valid_ID_3"),
    pytest.param(9001, 18, 7, 0, no_exception(), id="CRUD get_top_100_from_collections valid_ID_4"),
]


@pytest.mark.parametrize("collection_id,skip,take,expected_length,expected_exception", testcases)
def test_get_top_100_from_collection(collection_id: int, skip: int, take: int, expected_length: int, expected_exception: AbstractContextManager, session: Session):
    with expected_exception:
        top_100 = get_top_100_from_collection(session, collection_id, skip, take)
        assert isinstance(top_100, list)
        assert len(top_100) == expected_length
        assert all(isinstance(user, UserDB) for user in top_100)
        assert not any(user.alliance for user in top_100)
        for user_1, user_2 in zip(top_100, top_100[1:]):
            assert user_1.trophy >= user_2.trophy
