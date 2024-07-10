import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import has_alliance_history


test_cases = [
    # alliance_id, expected_result
    pytest.param(205906, True, id="true"),
    pytest.param(1, False, id="false"),
]


@pytest.mark.parametrize(["alliance_id", "expected_result"], test_cases)
async def test_has_alliance_history(alliance_id: int, expected_result: bool, session: AsyncSession):
    result = await has_alliance_history(session, alliance_id)
    assert result is expected_result
