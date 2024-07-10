from datetime import datetime, timezone

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import has_collection_with_timestamp


test_cases = [
    # timestamp, expected_result
    pytest.param(datetime(2024, 3, 31, 12, 59, 0), True, id="existing_timestamp_without_timezone"),
    pytest.param(datetime(2024, 3, 31, 12, 29, 0), False, id="not_existing_timestamp_without_timezone"),
    pytest.param(datetime(2024, 3, 31, 12, 59, 0, tzinfo=timezone.utc), True, id="existing_timestamp_with_timezone"),
    pytest.param(datetime(2024, 3, 31, 12, 29, 0, tzinfo=timezone.utc), False, id="not_existing_timestamp_with_timezone"),
]


@pytest.mark.parametrize(["timestamp", "expected_result"], test_cases)
async def test_has_collection_with_timestamp(timestamp: datetime, expected_result: bool, session: AsyncSession):
    result = await has_collection_with_timestamp(session, timestamp)
    assert result is expected_result
