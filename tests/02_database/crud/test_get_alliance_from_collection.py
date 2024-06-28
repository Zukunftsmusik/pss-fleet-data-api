from contextlib import AbstractContextManager
from contextlib import nullcontext as no_exception
from typing import Optional

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import get_alliance_from_collection
from src.api.database.models import AllianceDB, UserDB

testcases = [
    pytest.param(1, 205164, False, None, AllianceDB, no_exception(), id="CRUD get_alliance_from_collection valid_ids_1"),
    pytest.param(1, 205164, True, 10, AllianceDB, no_exception(), id="CRUD get_alliance_from_collection valid_ids_2"),
    pytest.param(8, 205164, True, 6, AllianceDB, no_exception(), id="CRUD get_alliance_from_collection valid_ids_3"),
    pytest.param(8, 201549, True, 15, AllianceDB, no_exception(), id="CRUD get_alliance_from_collection valid_ids_4"),
    pytest.param(1, 1, False, None, type(None), no_exception(), id="CRUD get_alliance_from_collection invalid_alliance_id_1"),
    pytest.param(1, 1, True, None, type(None), no_exception(), id="CRUD get_alliance_from_collection invalid_alliance_id_2"),
    pytest.param(9001, 21, False, None, type(None), no_exception(), id="CRUD get_alliance_from_collection invalid_collection_id_1"),
    pytest.param(9001, 21, True, None, type(None), no_exception(), id="CRUD get_alliance_from_collection invalid_collection_id_2"),
    pytest.param(9001, 1, False, None, type(None), no_exception(), id="CRUD get_alliance_from_collection invalid_ids_1"),
    pytest.param(9001, 1, True, None, type(None), no_exception(), id="CRUD get_alliance_from_collection invalid_ids_2"),
]


@pytest.mark.parametrize("collection_id,alliance_id,include_members,expected_user_count,expected_type,expected_exception", testcases)
async def test_get_alliance_from_collection(
    collection_id: int, alliance_id: int, include_members: bool, expected_user_count: Optional[int], expected_type: type, expected_exception: AbstractContextManager, session: AsyncSession
):
    with expected_exception:
        alliance = await get_alliance_from_collection(session, collection_id, alliance_id, include_members)
        assert isinstance(alliance, expected_type)
        if alliance:
            if include_members:
                assert len(alliance.users) == expected_user_count
                if expected_user_count:
                    assert isinstance(alliance.users[0], UserDB)
            else:
                assert not alliance.users
