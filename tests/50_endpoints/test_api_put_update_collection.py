import os
from typing import Any, Callable

import pytest
import test_cases
from fastapi.testclient import TestClient
from httpx import Response as HttpXResponse

from src.api import main
from src.api.models.enums import ErrorCode
from src.api.routers import dependencies


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
@pytest.mark.usefixtures("patch_has_collection_true")
@pytest.mark.parametrize(["path", "file_name", "expected_error_code"], test_cases.invalid_upload_files)
async def test_upload_invalid_JSON(
    path: str, file_name: str, expected_error_code: ErrorCode, assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient
):
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.put("/collections/upload/1", files=files)
            assert response.status_code == 422
            assert_error_code(response, expected_error_code)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
@pytest.mark.usefixtures("patch_has_collection_false")
@pytest.mark.parametrize(["path", "file_name"], test_cases.valid_update_files)
async def test_upload_collection_id_not_found(
    path: str, file_name: str, assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient
):
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.put("/collections/upload/1", files=files)
            assert response.status_code == 404
            assert_error_code(response, ErrorCode.COLLECTION_NOT_FOUND)


@pytest.mark.usefixtures("collection_metadata_out_json")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
@pytest.mark.usefixtures("patch_get_collection", "patch_has_collection_true", "patch_update_collection")
@pytest.mark.parametrize(["path", "file_name"], test_cases.valid_update_files)
async def test_upload_valid(path: str, file_name: str, collection_metadata_out_json: Any, client: TestClient):
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.put("/collections/upload/1", files=files)
            assert response.status_code == 200


@pytest.mark.parametrize(["headers"], test_cases.not_authenticated_headers)
def test_upload_not_authenticated(
    headers: dict[str, str], assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client_without_headers: TestClient
):
    path = "tests/test_data"
    file_name = "upload_test_data_schema_9.json"
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client_without_headers:
            response = client_without_headers.put("/collections/upload/1", files=files, headers=headers)
            assert response.status_code == 401
            assert_error_code(response, ErrorCode.NOT_AUTHENTICATED)


@pytest.mark.usefixtures("patch_check_is_authenticated_true")
def test_upload_not_authorized(assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    api_key = "123456"

    path = "tests/test_data"
    file_name = "upload_test_data_schema_9.json"
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.put(
                "/collections/upload/1",
                files=files,
                headers={
                    "Authorization": api_key,
                },
            )
            assert response.status_code == 403
            assert_error_code(response, ErrorCode.FORBIDDEN)


@pytest.mark.usefixtures("collection_metadata_out_json")
@pytest.mark.usefixtures("patch_get_collection", "patch_has_collection_true", "patch_root_api_key_123456", "patch_update_collection")
def test_upload_authenticated_and_authorized(collection_metadata_out_json: Any, client: TestClient):
    api_key = "123456"

    path = "tests/test_data"
    file_name = "update_test_data_schema_9.json"
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.put(
                "/collections/upload/1",
                files=files,
                headers={
                    "Authorization": api_key,
                },
            )

            assert response.status_code == 200


@pytest.mark.usefixtures("collection_metadata_out_json")
@pytest.mark.usefixtures("patch_get_collection", "patch_has_collection_true", "patch_update_collection")
@pytest.mark.parametrize(["root_api_key"], test_cases.root_api_keys)
def test_upload_no_authorization_required(root_api_key: str, collection_metadata_out_json: Any, client: TestClient):
    def override_root_api_key():
        return root_api_key

    main.app.dependency_overrides[dependencies.root_api_key] = override_root_api_key

    path = "tests/test_data"
    file_name = "update_test_data_schema_9.json"
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.put("/collections/upload/1", files=files)
            assert response.status_code == 200

    del main.app.dependency_overrides[dependencies.root_api_key]
