from typing import Callable

import pytest
import test_cases
from fastapi.testclient import TestClient
from httpx import Response as HttpXResponse

from src.api import main
from src.api.database import crud
from src.api.models.enums import ErrorCode
from src.api.routers import dependencies


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
@pytest.mark.parametrize(["collection_id"], test_cases.invalid_ids)
def test_delete_collection_invalid_id(collection_id: int, assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    with client:
        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 422
        assert_error_code(response, ErrorCode.PARAMETER_COLLECTION_ID_INVALID)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("collection_db", "collection_out_with_children")
@pytest.mark.usefixtures("patch_has_collection_true")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
def test_delete_collection_internal_server_error(assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient, monkeypatch):
    async def mock_delete_collection(*args):
        return False

    monkeypatch.setattr(crud, crud.delete_collection.__name__, mock_delete_collection)

    with client:
        response = client.delete("/collections/1")
        assert response.status_code == 500
        assert_error_code(response, ErrorCode.COLLECTION_NOT_DELETED)


@pytest.mark.usefixtures("patch_has_collection_false", "assert_error_code")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
def test_delete_collection_non_existing_id(assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    with client:
        response = client.delete("/collections/1")
        assert response.status_code == 404
        assert_error_code(response, ErrorCode.COLLECTION_NOT_FOUND)


@pytest.mark.parametrize(["collection_id"], test_cases.valid_ids)
@pytest.mark.usefixtures("patch_has_collection_true")
@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
def test_delete_collection_valid_id(collection_id: int, client: TestClient, monkeypatch):
    async def mock_delete_collection(*args):
        return True

    monkeypatch.setattr(crud, crud.delete_collection.__name__, mock_delete_collection)

    with client:
        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 204


@pytest.mark.parametrize(["headers"], test_cases.not_authenticated_headers)
def test_delete_collection_not_authenticated(
    headers: dict[str, str], assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client_without_headers: TestClient
):
    with client_without_headers:
        response = client_without_headers.delete("/collections/1", headers=headers)
        assert response.status_code == 401
        assert_error_code(response, ErrorCode.NOT_AUTHENTICATED)


@pytest.mark.usefixtures("patch_check_is_authenticated_true")
def test_delete_collection_not_authorized(assert_error_code: Callable[[HttpXResponse, ErrorCode], None], client: TestClient):
    with client:
        response = client.delete("/collections/1")

        assert response.status_code == 403
        assert_error_code(response, ErrorCode.FORBIDDEN)


@pytest.mark.usefixtures("patch_delete_collection_true", "patch_has_collection_true", "patch_root_api_key_123456")
def test_delete_collection_authenticated_and_authorized(client: TestClient):
    api_key = "123456"

    with client:
        response = client.delete(
            "/collections/1",
            headers={
                "Authorization": api_key,
            },
        )

        assert response.status_code == 204


@pytest.mark.usefixtures("patch_delete_collection_true", "patch_has_collection_true")
@pytest.mark.parametrize(["root_api_key"], test_cases.root_api_keys)
def test_delete_collection_no_authorization_required(root_api_key: str, client: TestClient):
    def override_root_api_key():
        return root_api_key

    main.app.dependency_overrides[dependencies.root_api_key] = override_root_api_key

    with client:
        response = client.delete("/collections/1")

        assert response.status_code == 204

    del main.app.dependency_overrides[dependencies.root_api_key]
