from contextlib import AbstractContextManager
from contextlib import nullcontext as no_exception

import pytest
from sqlmodel import Session

from src.api.database.crud import delete_collection
from src.api.database.models import CollectionDB

testcases = [
    pytest.param(1, True, no_exception(), id="CRUD delete_collection valid_id"),
    pytest.param(9001, False, no_exception(), id="CRUD delete_collection invalid_id"),
]


@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("collection_id,expected_result,expected_exception", testcases)
def test_get_alliance_from_collection(collection_id: int, expected_result: bool, expected_exception: AbstractContextManager, session: Session) -> CollectionDB:
    with expected_exception:
        result = delete_collection(session, collection_id)
        assert result == expected_result
