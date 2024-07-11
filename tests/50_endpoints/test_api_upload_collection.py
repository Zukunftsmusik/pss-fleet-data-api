import os
from typing import Any

import pytest
import test_cases
from fastapi.testclient import TestClient

from src.api import main
from src.api.models.enums import ErrorCode
from src.api.routers import dependencies


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
@pytest.mark.parametrize(["path", "file_name", "expected_error_code"], test_cases.invalid_upload_files)
async def test_upload_invalid_JSON(path: str, file_name: str, expected_error_code: ErrorCode, assert_error_code, client: TestClient):
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.post("/collections/upload", files=files)
            assert response.status_code == 422
            assert_error_code(response, expected_error_code)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
@pytest.mark.usefixtures("patch_get_collection_by_timestamp")
@pytest.mark.parametrize(["path", "file_name"], test_cases.valid_upload_files)
async def test_upload_non_unique_timestamp(path: str, file_name: str, assert_error_code, client: TestClient):
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.post("/collections/upload", files=files)
            assert response.status_code == 409
            assert_error_code(response, ErrorCode.NON_UNIQUE_TIMESTAMP)


@pytest.mark.usefixtures("collection_metadata_out_json")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
@pytest.mark.usefixtures("patch_get_collection_by_timestamp_none", "patch_save_collection")
@pytest.mark.parametrize(["path", "file_name"], test_cases.valid_upload_files)
async def test_upload_valid(path: str, file_name: str, collection_metadata_out_json: Any, client: TestClient):
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.post("/collections/upload", files=files)
            assert response.status_code == 201
            assert response.json() == collection_metadata_out_json


def test_upload_not_authenticated(assert_error_code, client: TestClient):
    path = "tests/test_data"
    file_name = "upload_test_data_schema_9.json"
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.post("/collections/upload", files=files)
            assert response.status_code == 401
            assert_error_code(response, ErrorCode.NOT_AUTHENTICATED)


@pytest.mark.usefixtures("patch_check_is_authenticated_true")
def test_upload_not_authorized(assert_error_code, client: TestClient):
    api_key = "123456"

    path = "tests/test_data"
    file_name = "upload_test_data_schema_9.json"
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.post(
                "/collections/upload",
                files=files,
                headers={
                    "Authorization": api_key,
                },
            )
            assert response.status_code == 403
            assert_error_code(response, ErrorCode.FORBIDDEN)


@pytest.mark.usefixtures("collection_metadata_out_json")
@pytest.mark.usefixtures("patch_get_collection_by_timestamp_none", "patch_root_api_key_123456", "patch_save_collection")
def test_upload_authenticated_and_authorized(collection_metadata_out_json: Any, client: TestClient):
    api_key = "123456"

    path = "tests/test_data"
    file_name = "upload_test_data_schema_9.json"
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.post(
                "/collections/upload",
                files=files,
                headers={
                    "Authorization": api_key,
                },
            )

            assert response.status_code == 201
            assert response.json() == collection_metadata_out_json


@pytest.mark.usefixtures("collection_metadata_out_json")
@pytest.mark.usefixtures("patch_get_collection_by_timestamp_none", "patch_save_collection")
@pytest.mark.parametrize(["root_api_key"], test_cases.root_api_keys)
def test_upload_no_authorization_required(root_api_key: str, collection_metadata_out_json: Any, client: TestClient):
    def override_root_api_key():
        return root_api_key

    main.app.dependency_overrides[dependencies.root_api_key] = override_root_api_key

    path = "tests/test_data"
    file_name = "upload_test_data_schema_9.json"
    file_path = os.path.join(path, file_name)

    with open(file_path, "rb") as fp:
        files = {"collection_file": (file_name, fp, "application/json")}
        with client:
            response = client.post("/collections/upload", files=files)
            assert response.status_code == 201
            assert response.json() == collection_metadata_out_json

    del main.app.dependency_overrides[dependencies.root_api_key]
