from contextlib import AbstractContextManager
from contextlib import nullcontext as no_exception

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import delete_collection

testcases = [
    pytest.param(1, True, no_exception(), id="CRUD delete_collection valid_id"),
    pytest.param(9001, False, no_exception(), id="CRUD delete_collection invalid_id"),
]


@pytest.mark.parametrize("collection_id,expected_result,expected_exception", testcases)
async def test_delete_collection(collection_id: int, expected_result: bool, expected_exception: AbstractContextManager, session: AsyncSession):
    with expected_exception:
        result = await delete_collection(session, collection_id)
        assert result == expected_result
