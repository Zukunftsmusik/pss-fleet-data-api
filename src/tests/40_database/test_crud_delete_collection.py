import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import delete_collection


test_cases = [
    # collection_id, expected_result
    pytest.param(1, True, id="valid_id"),
    pytest.param(9001, False, id="invalid_id"),
]


@pytest.mark.parametrize(["collection_id", "expected_result"], test_cases)
async def test_delete_collection(collection_id: int, expected_result: bool, session: AsyncSession):
    result = await delete_collection(session, collection_id)
    assert result == expected_result
