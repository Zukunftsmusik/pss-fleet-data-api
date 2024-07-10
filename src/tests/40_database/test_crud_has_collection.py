import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import has_collection


test_cases = [
    # collection_id, expected_result
    pytest.param(1, True, id="true"),
    pytest.param(9001, False, id="false"),
]


@pytest.mark.parametrize(["collection_id", "expected_result"], test_cases)
async def test_has_collection(collection_id: int, expected_result: bool, session: AsyncSession):
    result = await has_collection(session, collection_id)
    assert result is expected_result
