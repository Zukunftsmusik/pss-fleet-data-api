from typing import Optional

import pytest

from src.api.routers import dependencies


test_cases_is_authenticated = [
    # api_key, expected_result
    pytest.param(None, False, id="api_key_is_None"),
    pytest.param("", False, id="api_key_is_empty"),
    pytest.param("123456", True, id="api_key_is_valid"),
]


test_cases_is_authorized = [
    # api_key, root_api_key, expected_result
    pytest.param("123456", "abcdef", False, id="not_authorized"),
    pytest.param("123456", "123456", True, id="authorized"),
]


@pytest.mark.parametrize(["api_key", "expected_result"], test_cases_is_authenticated)
def test_check_is_authenticated(api_key: Optional[str], expected_result: bool):
    assert dependencies._check_is_authenticated(api_key) is expected_result


@pytest.mark.parametrize(["api_key", "root_api_key", "expected_result"], test_cases_is_authorized)
def test_check_is_authorized(api_key: str, root_api_key: str, expected_result: bool):
    assert dependencies._check_is_authorized(None, api_key, root_api_key) is expected_result
