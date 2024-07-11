from datetime import datetime
from typing import Any, Union

import pytest
import test_cases
from fastapi.testclient import TestClient

from src.api.models.enums import ErrorCode, ParameterInterval


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.parametrize(["parameters", "expected_error_code"], test_cases.invalid_filter_parameters)
def test_get_collections_invalid_parameters(
    parameters: dict[str, Union[bool, datetime, int, ParameterInterval]], expected_error_code: ErrorCode, assert_error_code, client: TestClient
):
    with client:
        response = client.get("/collections", params=parameters)
        assert response.status_code == 422
        assert_error_code(response, expected_error_code)


@pytest.mark.usefixtures("collection_metadata_out_json")
@pytest.mark.usefixtures("patch_get_collections")
@pytest.mark.parametrize(["_", "parameters", "headers"], test_cases.valid_id_and_filter_parameters)
def test_get_collections_valid_parameters(
    _,
    parameters: dict[str, Union[bool, datetime, int, ParameterInterval]],
    headers: dict[str, str],
    collection_metadata_out_json: Any,
    client: TestClient,
):
    with client:
        response = client.get(
            "/collections",
            params=parameters,
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json() == [collection_metadata_out_json]
