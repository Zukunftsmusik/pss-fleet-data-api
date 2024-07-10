import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import has_user_history


test_cases = [
    # user_id, expected_result
    pytest.param(20013541, True, id="true"),
    pytest.param(1, False, id="false"),
]


@pytest.mark.parametrize(["user_id", "expected_result"], test_cases)
async def test_has_user_history(user_id: int, expected_result: bool, session: AsyncSession):
    result = await has_user_history(session, user_id)
    assert result is expected_result
