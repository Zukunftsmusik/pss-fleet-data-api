from contextlib import AbstractContextManager
from contextlib import nullcontext as no_exception

import pytest
from sqlmodel import Session

from src.api.database.crud import get_collection
from src.api.database.models import AllianceDB, CollectionDB, UserDB

testcases = [
    pytest.param(1, False, False, CollectionDB, no_exception(), id="CRUD get_collection valid_ID_1"),
    pytest.param(1, True, False, CollectionDB, no_exception(), id="CRUD get_collections valid_ID_2"),
    pytest.param(1, False, True, CollectionDB, no_exception(), id="CRUD get_collections valid_ID_3"),
    pytest.param(1, True, True, CollectionDB, no_exception(), id="CRUD get_collections valid_ID_4"),
    pytest.param(9001, False, False, type(None), no_exception(), id="CRUD get_collections invalid_ID_1"),
    pytest.param(9001, True, False, type(None), no_exception(), id="CRUD get_collections invalid_ID_2"),
    pytest.param(9001, False, True, type(None), no_exception(), id="CRUD get_collections invalid_ID_3"),
    pytest.param(9001, True, True, type(None), no_exception(), id="CRUD get_collections invalid_ID_4"),
]


@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("collection_id,include_alliances,include_users,expected_type,expected_exception", testcases)
def test_get_collection(collection_id: int, include_alliances: bool, include_users: bool, expected_type: type, expected_exception: AbstractContextManager, session: Session):
    with expected_exception:
        collection = get_collection(session, collection_id, include_alliances, include_users)
        assert isinstance(collection, expected_type)
        if collection:
            if include_alliances:
                assert collection.alliances
                assert isinstance(collection.alliances[0], AllianceDB)
            if include_users:
                assert collection.users
                assert isinstance(collection.users[0], UserDB)
