from typing import Any, Callable

import pytest
import test_cases
from fastapi.testclient import TestClient
from httpx import Response as HttpXResponse

from src.api.models.enums import ErrorCode


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.parametrize(["collection_id"], test_cases.invalid_ids)
def test_get_collection_invalid_id(collection_id: int, assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    with client:
        response = client.get(f"/collections/{collection_id}")
        assert response.status_code == 422
        assert_error_code(response, ErrorCode.PARAMETER_COLLECTION_ID_INVALID)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_get_collection_none")
def test_get_collection_non_existing_id(assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    with client:
        response = client.get("/collections/1")
        assert response.status_code == 404
        assert_error_code(response, ErrorCode.COLLECTION_NOT_FOUND)


@pytest.mark.usefixtures("collection_out_with_children_json")
@pytest.mark.usefixtures("patch_get_collection")
@pytest.mark.parametrize(["collection_id"], test_cases.valid_ids)
def test_get_collection_valid_id(collection_id: int, collection_out_with_children_json: Any, client: TestClient):
    with client:
        response = client.get(f"/collections/{collection_id}")
        assert response.status_code == 200
        assert response.json() == collection_out_with_children_json
