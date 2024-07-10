from typing import Any

import pytest
import test_cases
from fastapi.testclient import TestClient

from src.api.database import crud
from src.api.database.models import UserDB
from src.api.models.enums import ErrorCode


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.parametrize(["collection_id", "user_id", "expected_error_code"], test_cases.invalid_collection_and_user_ids)
def test_get_user_from_collection_invalid_ids(
    collection_id: int, user_id: int, expected_error_code: ErrorCode, assert_error_code, client: TestClient
):
    with client:
        response = client.get(f"/collections/{collection_id}/users/{user_id}")
        assert response.status_code == 422
        assert_error_code(response, expected_error_code)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("user_db")
@pytest.mark.parametrize(["collection_exists", "user_exists", "expected_error_code"], test_cases.does_exist_collection_and_user)
def test_get_user_from_collection_non_existing_ids(
    user_db: UserDB, collection_exists: bool, user_exists: bool, expected_error_code: ErrorCode, assert_error_code, client: TestClient, monkeypatch
):
    async def mock_has_collection(*args):
        return collection_exists

    async def mock_get_user_from_collection(*args):
        if user_exists:
            return user_db
        else:
            return None

    monkeypatch.setattr(crud, crud.has_collection.__name__, mock_has_collection)
    monkeypatch.setattr(crud, crud.get_user_from_collection.__name__, mock_get_user_from_collection)

    with client:
        response = client.get("/collections/1/users/1")
        assert response.status_code == 404
        assert_error_code(response, expected_error_code)


@pytest.mark.usefixtures("user_history_out_json")
@pytest.mark.usefixtures("patch_get_user_from_collection", "patch_has_collection_true")
@pytest.mark.parametrize(["collection_id", "user_id"], test_cases.valid_collection_and_child_ids)
def test_get_user_from_collection_valid_ids(collection_id: int, user_id: int, user_history_out_json: Any, client: TestClient):
    with client:
        response = client.get(f"/collections/{collection_id}/users/{user_id}")
        assert response.status_code == 200
        assert response.json() == user_history_out_json
