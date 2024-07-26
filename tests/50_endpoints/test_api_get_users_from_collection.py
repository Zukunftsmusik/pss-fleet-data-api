from typing import Any, Callable

import pytest
import test_cases
from fastapi.testclient import TestClient
from httpx import Response as HttpXResponse

from src.api.models.enums import ErrorCode


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.parametrize(["collection_id"], test_cases.invalid_ids)
def test_get_users_from_collection_invalid_id(collection_id: int, assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    with client:
        response = client.get(f"/collections/{collection_id}/users")
        assert response.status_code == 422
        assert_error_code(response, ErrorCode.PARAMETER_COLLECTION_ID_INVALID)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_has_collection_false")
def test_get_users_from_collection_non_existing_id(assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    with client:
        response = client.get("/collections/1/users")
        assert response.status_code == 404
        assert_error_code(response, ErrorCode.COLLECTION_NOT_FOUND)


@pytest.mark.usefixtures("collection_with_users_out_json")
@pytest.mark.usefixtures("patch_get_collection", "patch_has_collection_true")
@pytest.mark.parametrize(["collection_id"], test_cases.valid_ids)
def test_get_users_from_collection_valid_id(collection_id: int, collection_with_users_out_json: Any, client: TestClient):
    with client:
        response = client.get(f"/collections/{collection_id}/users")
        assert response.status_code == 200
        assert response.json() == collection_with_users_out_json
