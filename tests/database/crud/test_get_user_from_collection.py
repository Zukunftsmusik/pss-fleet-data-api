from contextlib import AbstractContextManager
from contextlib import nullcontext as no_exception

import pytest
from sqlmodel import Session

from src.api.database.crud import get_user_from_collection
from src.api.database.models import UserDB

testcases = [
    pytest.param(1, 20013541, False, UserDB, no_exception(), id="CRUD get_user_from_collection valid_ids_1"),
    pytest.param(1, 20013541, True, UserDB, no_exception(), id="CRUD get_user_from_collection valid_ids_2"),
    pytest.param(8, 20013541, True, UserDB, no_exception(), id="CRUD get_user_from_collection valid_ids_3"),
    pytest.param(8, 20013541, True, UserDB, no_exception(), id="CRUD get_user_from_collection valid_ids_4"),
    pytest.param(1, 1, False, type(None), no_exception(), id="CRUD get_user_from_collection invalid_user_id_1"),
    pytest.param(1, 1, True, type(None), no_exception(), id="CRUD get_user_from_collection invalid_user_id_2"),
    pytest.param(9001, 20013541, False, type(None), no_exception(), id="CRUD get_user_from_collection invalid_collection_id_1"),
    pytest.param(9001, 20013541, True, type(None), no_exception(), id="CRUD get_user_from_collection invalid_collection_id_2"),
    pytest.param(9001, 1, False, type(None), no_exception(), id="CRUD get_user_from_collection invalid_ids_1"),
    pytest.param(9001, 1, True, type(None), no_exception(), id="CRUD get_user_from_collection invalid_ids_2"),
]


@pytest.mark.usefixtures("session")
@pytest.mark.parametrize("collection_id,user_id,include_alliance,expected_type,expected_exception", testcases)
def test_get_user_from_collection(collection_id: int, user_id: int, include_alliance: bool, expected_type: type, expected_exception: AbstractContextManager, session: Session):
    with expected_exception:
        user = get_user_from_collection(session, collection_id, user_id, include_alliance)
        assert isinstance(user, expected_type)
        if user:
            assert bool(user.alliance) == include_alliance
