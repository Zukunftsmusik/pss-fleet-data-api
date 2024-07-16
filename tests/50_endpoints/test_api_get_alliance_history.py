from datetime import datetime
from typing import Callable, Union

import pytest
import test_cases
from fastapi.testclient import TestClient
from httpx import Response as HttpXResponse

from src.api.models.enums import ErrorCode, ParameterInterval


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.parametrize(["parameters", "expected_error_code"], test_cases.invalid_filter_parameters)
def test_get_alliance_history_invalid_parameters(
    parameters: dict[str, Union[bool, datetime, int, ParameterInterval]],
    expected_error_code: ErrorCode,
    assert_error_code: Callable[[HttpXResponse, ErrorCode], None],
    client: TestClient,
):
    with client:
        response = client.get("/allianceHistory/1", params=parameters)
        assert response.status_code == 422
        assert_error_code(response, expected_error_code)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.parametrize(["alliance_id"], test_cases.invalid_ids)
def test_get_alliance_history_invalid_id(alliance_id: int, assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    with client:
        response = client.get(f"/allianceHistory/{alliance_id}")
        assert response.status_code == 422
        assert_error_code(response, ErrorCode.PARAMETER_ALLIANCE_ID_INVALID)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_has_alliance_history_false")
def test_get_alliance_history_non_existing_id(assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    with client:
        response = client.get("/allianceHistory/1")
        assert response.status_code == 404
        assert_error_code(response, ErrorCode.ALLIANCE_NOT_FOUND)


@pytest.mark.usefixtures("alliance_history_out_json")
@pytest.mark.usefixtures("patch_has_alliance_history_true", "patch_get_alliance_history")
@pytest.mark.parametrize(["alliance_id", "parameters", "headers"], test_cases.valid_id_and_filter_parameters)
def test_get_alliance_history_valid_parameters(
    alliance_id: int,
    parameters: dict[str, Union[bool, datetime, int, ParameterInterval]],
    headers: dict[str, str],
    alliance_history_out_json,
    client: TestClient,
):
    with client:
        response = client.get(
            f"/allianceHistory/{alliance_id}",
            params=parameters,
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json() == [alliance_history_out_json]
