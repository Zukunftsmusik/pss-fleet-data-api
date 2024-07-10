from typing import Any

import pytest
import test_cases
from fastapi.testclient import TestClient

from src.api import main
from src.api.models import CollectionCreate9
from src.api.models.enums import ErrorCode
from src.api.routers import dependencies


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
@pytest.mark.parametrize(["invalid_payload"], test_cases.invalid_save_collection_payloads())
def test_create_collection_invalid_payload(invalid_payload: CollectionCreate9, assert_error_code, client: TestClient):
    content = invalid_payload.model_dump_json()

    with client:
        response = client.post("/collections", content=content)
        assert response.status_code == 422
        assert_error_code(response, ErrorCode.UNSUPPORTED_SCHEMA)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("collection_create_9")
@pytest.mark.usefixtures("patch_get_collection_by_timestamp", "patch_check_is_authenticated_true", "patch_check_is_authorized_true")
async def test_create_collection_non_unique_timestamp(collection_create_9: CollectionCreate9, assert_error_code, client: TestClient):
    with client:
        response = client.post("/collections", content=collection_create_9.model_dump_json())
        assert response.status_code == 409
        assert_error_code(response, ErrorCode.NON_UNIQUE_TIMESTAMP)


@pytest.mark.usefixtures("collection_create_9", "collection_metadata_out_json")
@pytest.mark.usefixtures(
    "patch_get_collection_by_timestamp_none", "patch_check_is_authenticated_true", "patch_check_is_authorized_true", "patch_save_collection"
)
def test_create_collection_valid_payload(collection_create_9: CollectionCreate9, collection_metadata_out_json: Any, client: TestClient):
    with client:
        response = client.post(
            "/collections",
            content=collection_create_9.model_dump_json(),
        )

        assert response.status_code == 201
        assert response.json() == collection_metadata_out_json


@pytest.mark.usefixtures("collection_create_9")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
@pytest.mark.parametrize(["method"], test_cases.invalid_save_collection_methods)
def test_create_collection_wrong_method(collection_create_9: CollectionCreate9, method: str, assert_error_code, client: TestClient):
    with client:
        response = client.request(method, "/collections", content=collection_create_9.model_dump_json())
        assert response.status_code == 405
        assert_error_code(response, ErrorCode.METHOD_NOT_ALLOWED)


@pytest.mark.usefixtures("collection_create_9")
def test_create_collection_not_authenticated(collection_create_9: CollectionCreate9, assert_error_code, client: TestClient):
    with client:
        response = client.post("/collections", content=collection_create_9.model_dump_json())
        assert response.status_code == 401
        assert_error_code(response, ErrorCode.NOT_AUTHENTICATED)


@pytest.mark.usefixtures("collection_create_9")
@pytest.mark.usefixtures("patch_check_is_authenticated_true")
def test_create_collection_not_authorized(collection_create_9: CollectionCreate9, assert_error_code, client: TestClient):
    with client:
        response = client.post("/collections", content=collection_create_9.model_dump_json())

        assert response.status_code == 403
        assert_error_code(response, ErrorCode.FORBIDDEN)


@pytest.mark.usefixtures("collection_create_9", "collection_metadata_out_json")
@pytest.mark.usefixtures("patch_get_collection_by_timestamp_none", "patch_root_api_key_123456", "patch_save_collection")
def test_create_collection_authenticated_and_authorized(
    collection_create_9: CollectionCreate9, collection_metadata_out_json: Any, client: TestClient
):
    api_key = "123456"

    with client:
        response = client.post(
            "/collections",
            content=collection_create_9.model_dump_json(),
            headers={
                "Authorization": api_key,
            },
        )

        assert response.status_code == 201
        assert response.json() == collection_metadata_out_json


@pytest.mark.usefixtures("collection_create_9", "collection_metadata_out_json")
@pytest.mark.usefixtures("patch_get_collection_by_timestamp_none", "patch_save_collection")
@pytest.mark.parametrize(["root_api_key"], test_cases.root_api_keys)
def test_create_collection_no_authorization_required(
    root_api_key: str, collection_create_9: CollectionCreate9, collection_metadata_out_json: Any, client: TestClient
):
    def override_root_api_key():
        return root_api_key

    main.app.dependency_overrides[dependencies.root_api_key] = override_root_api_key

    with client:
        response = client.post("/collections", content=collection_create_9.model_dump_json())

        assert response.status_code == 201
        assert response.json() == collection_metadata_out_json

    del main.app.dependency_overrides[dependencies.root_api_key]
