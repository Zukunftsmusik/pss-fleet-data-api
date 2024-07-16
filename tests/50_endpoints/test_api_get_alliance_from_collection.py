from typing import Any, Callable

import pytest
import test_cases
from fastapi.testclient import TestClient
from httpx import Response as HttpXResponse

from src.api.database import crud
from src.api.database.models import AllianceDB
from src.api.models.enums import ErrorCode


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.parametrize(["collection_id", "alliance_id", "expected_error_code"], test_cases.invalid_collection_and_alliance_ids)
def test_get_alliance_from_collection_invalid_ids(
    collection_id: int,
    alliance_id: int,
    expected_error_code: ErrorCode,
    assert_error_code: Callable[[HttpXResponse, ErrorCode], None],
    client: TestClient,
):
    with client:
        response = client.get(f"/collections/{collection_id}/alliances/{alliance_id}")
        assert response.status_code == 422
        assert_error_code(response, expected_error_code)


@pytest.mark.usefixtures("assert_error_code")
@pytest.mark.usefixtures("alliance_db")
@pytest.mark.parametrize(["collection_exists", "alliance_exists", "expected_error_code"], test_cases.does_exist_collection_and_alliance)
def test_get_alliance_from_collection_non_existing_ids(
    alliance_db: AllianceDB,
    collection_exists: bool,
    alliance_exists: bool,
    expected_error_code: ErrorCode,
    assert_error_code,
    client: TestClient,
    monkeypatch,
):
    async def mock_has_collection(*args):
        return collection_exists

    async def mock_get_alliance_from_collection(*args):
        if alliance_exists:
            return alliance_db
        else:
            return None

    monkeypatch.setattr(crud, crud.has_collection.__name__, mock_has_collection)
    monkeypatch.setattr(crud, crud.get_alliance_from_collection.__name__, mock_get_alliance_from_collection)

    with client:
        response = client.get("/collections/1/alliances/1")
        assert response.status_code == 404
        assert_error_code(response, expected_error_code)


@pytest.mark.usefixtures("alliance_history_out_json")
@pytest.mark.usefixtures("patch_get_alliance_from_collection", "patch_has_collection_true")
@pytest.mark.parametrize(["collection_id", "alliance_id"], test_cases.valid_collection_and_child_ids)
def test_get_alliance_from_collection_valid_ids(collection_id: int, alliance_id: int, alliance_history_out_json: Any, client: TestClient):
    with client:
        response = client.get(f"/collections/{collection_id}/alliances/{alliance_id}")
        assert response.status_code == 200
        assert response.json() == alliance_history_out_json
