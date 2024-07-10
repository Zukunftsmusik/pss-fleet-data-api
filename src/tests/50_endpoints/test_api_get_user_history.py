from datetime import datetime
from typing import Any, Union

import pytest
import test_cases
from fastapi.testclient import TestClient

from src.api.models.enums import ErrorCode, ParameterInterval


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.parametrize(["parameters", "expected_error_code"], test_cases.invalid_filter_parameters)
def test_get_user_history_invalid_parameters(
    parameters: dict[str, Union[bool, datetime, int, ParameterInterval]], expected_error_code: ErrorCode, assert_error_code, client: TestClient
):
    with client:
        response = client.get("/userHistory/1", params=parameters)
        assert response.status_code == 422
        assert_error_code(response, expected_error_code)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.parametrize(["user_id"], test_cases.invalid_ids)
def test_get_user_history_invalid_user_id(user_id: int, assert_error_code, client: TestClient):
    with client:
        response = client.get(f"/userHistory/{user_id}")
        assert response.status_code == 422
        assert_error_code(response, ErrorCode.PARAMETER_USER_ID_INVALID)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_has_user_history_false")
def test_get_user_history_non_existing_id(assert_error_code, client: TestClient):
    with client:
        response = client.get("/userHistory/1")
        assert response.status_code == 404
        assert_error_code(response, ErrorCode.USER_NOT_FOUND)


@pytest.mark.usefixtures("user_history_db", "user_history_out")
@pytest.mark.usefixtures("patch_has_user_history_true", "patch_get_user_history")
@pytest.mark.parametrize(["user_id", "parameters"], test_cases.valid_id_and_filter_parameters)
def test_get_user_history_valid_parameters(
    user_id: int, parameters: dict[str, Union[bool, datetime, int, ParameterInterval]], user_history_out_json: Any, client: TestClient
):
    with client:
        response = client.get(f"/userHistory/{user_id}", params=parameters)
        assert response.status_code == 200
        assert response.json() == [user_history_out_json]
