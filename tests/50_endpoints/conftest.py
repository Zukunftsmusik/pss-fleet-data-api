import json
from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient
from httpx import Response as HttpXResponse

from src.api import main
from src.api.database import crud
from src.api.database.models import CollectionDB
from src.api.models import AllianceHistoryOut, AllianceOut, CollectionOut, CollectionWithFleetsOut, CollectionWithUsersOut, UserHistoryOut, UserOut
from src.api.models.converters import FromDB
from src.api.models.enums import ErrorCode
from src.api.models.error import ErrorOut
from src.api.routers import dependencies


# Response objects


@pytest.fixture(scope="function")
def alliance_history_out(alliance_history_db) -> AllianceHistoryOut:
    return FromDB.to_alliance_history(alliance_history_db)


@pytest.fixture(scope="function")
def alliance_history_out_json(alliance_history_out: AllianceHistoryOut) -> Any:
    return json.loads(alliance_history_out.model_dump_json())


@pytest.fixture(scope="function")
def alliance_out(alliance_db) -> AllianceOut:
    return FromDB.to_alliance(alliance_db)


@pytest.fixture(scope="function")
def alliance_out_json(alliance_out: AllianceOut) -> Any:
    return list(alliance_out)


@pytest.fixture(scope="session", autouse=True)
def client():
    client = TestClient(
        main.app,
        headers={"Authorization": ""},
    )
    yield client


@pytest.fixture(scope="function")
def collection_metadata_out_json(collection_out_without_children: CollectionOut) -> Any:
    return json.loads(collection_out_without_children.metadata.model_dump_json())


@pytest.fixture(scope="function")
def collection_out_with_children(collection_db) -> CollectionOut:
    return FromDB.to_collection(collection_db, True, True)


@pytest.fixture(scope="function")
def collection_out_with_children_json(collection_out_with_children: CollectionOut) -> Any:
    return json.loads(collection_out_with_children.model_dump_json())


@pytest.fixture(scope="function")
def collection_with_fleets_out(collection_db) -> CollectionWithFleetsOut:
    return CollectionWithFleetsOut(**(FromDB.to_collection(collection_db, True, False).model_dump()))


@pytest.fixture(scope="function")
def collection_with_fleets_out_json(collection_with_fleets_out: CollectionOut) -> Any:
    return json.loads(collection_with_fleets_out.model_dump_json())


@pytest.fixture(scope="function")
def collection_with_users_out(collection_db) -> CollectionOut:
    return CollectionWithUsersOut(**(FromDB.to_collection(collection_db, False, True).model_dump()))


@pytest.fixture(scope="function")
def collection_with_users_out_json(collection_with_users_out: CollectionOut) -> Any:
    return json.loads(collection_with_users_out.model_dump_json())


@pytest.fixture(scope="function")
def collection_out_without_children(collection_db) -> CollectionOut:
    return FromDB.to_collection(collection_db, False, False)


@pytest.fixture(scope="function")
def collection_out_without_children_json(collection_out_without_children: CollectionOut) -> Any:
    return json.loads(collection_out_without_children.model_dump_json())


@pytest.fixture(scope="function")
def user_history_out(user_history_db) -> UserHistoryOut:
    return FromDB.to_user_history(user_history_db)


@pytest.fixture(scope="function")
def user_history_out_json(user_history_out: UserHistoryOut) -> Any:
    return json.loads(user_history_out.model_dump_json())


@pytest.fixture(scope="function")
def user_out(user_db) -> UserOut:
    return FromDB.to_user(user_db)


@pytest.fixture(scope="function")
def user_out_json(user_out: UserOut) -> UserOut:
    return list(user_out)


# Mocks


@pytest.fixture(scope="function")
def patch_check_is_authenticated_true(monkeypatch):
    def mock_check_is_authenticated(*args):
        return True

    monkeypatch.setattr(dependencies, dependencies._check_is_authenticated.__name__, mock_check_is_authenticated)


@pytest.fixture(scope="function")
def patch_check_is_authorized_true(monkeypatch):
    def mock_check_is_authorized(*args):
        return True

    monkeypatch.setattr(dependencies, dependencies._check_is_authorized.__name__, mock_check_is_authorized)


@pytest.fixture(scope="function")
def patch_delete_collection_true(monkeypatch):
    async def mock_delete_collection(*args):
        return True

    monkeypatch.setattr(crud, crud.delete_collection.__name__, mock_delete_collection)


@pytest.fixture(scope="function")
def patch_get_alliance_history(alliance_history_db, monkeypatch):
    async def mock_get_alliance_history(*args):
        return [alliance_history_db]

    monkeypatch.setattr(crud, crud.get_alliance_history.__name__, mock_get_alliance_history)


@pytest.fixture(scope="function")
def patch_get_alliance_from_collection(alliance_history_db, monkeypatch):
    async def mock_get_alliance_from_collection(*args):
        return alliance_history_db

    monkeypatch.setattr(crud, crud.get_alliance_from_collection.__name__, mock_get_alliance_from_collection)


@pytest.fixture(scope="function")
def patch_get_collection_none(monkeypatch):
    async def mock_get_collection(*args):
        return None

    monkeypatch.setattr(crud, crud.get_collection.__name__, mock_get_collection)


@pytest.fixture(scope="function")
def patch_get_collection(collection_db: CollectionDB, monkeypatch):
    async def mock_get_collection(session, collection_id, include_alliances, include_users):
        if not include_alliances:
            collection_db.alliances = []
        if not include_users:
            collection_db.users = []
        return collection_db

    monkeypatch.setattr(crud, crud.get_collection.__name__, mock_get_collection)


@pytest.fixture(scope="function")
def patch_get_collection_by_timestamp(collection_db: CollectionDB, monkeypatch):
    async def mock_get_collection_by_timestamp(*args):
        return collection_db

    monkeypatch.setattr(crud, crud.get_collection_by_timestamp.__name__, mock_get_collection_by_timestamp)


@pytest.fixture(scope="function")
def patch_get_collection_by_timestamp_none(collection_db: CollectionDB, monkeypatch):
    async def mock_get_collection_by_timestamp(*args):
        return None

    monkeypatch.setattr(crud, crud.get_collection_by_timestamp.__name__, mock_get_collection_by_timestamp)


@pytest.fixture(scope="function")
def patch_get_collections(collection_db, monkeypatch):
    async def mock_get_collections(*args):
        return [collection_db]

    monkeypatch.setattr(crud, crud.get_collections.__name__, mock_get_collections)


@pytest.fixture(scope="function")
def patch_get_top_100_from_collection(user_db, monkeypatch):
    async def mock_get_top_100_from_collection(*args):
        return [user_db]

    monkeypatch.setattr(crud, crud.get_top_100_from_collection.__name__, mock_get_top_100_from_collection)


@pytest.fixture(scope="function")
def patch_get_user_from_collection(user_history_db, monkeypatch):
    async def mock_get_user_from_collection(*args):
        return user_history_db

    monkeypatch.setattr(crud, crud.get_user_from_collection.__name__, mock_get_user_from_collection)


@pytest.fixture(scope="function")
def patch_get_user_history(user_history_db, monkeypatch):
    async def mock_get_user_history(*args):
        return [user_history_db]

    monkeypatch.setattr(crud, crud.get_user_history.__name__, mock_get_user_history)


@pytest.fixture(scope="function")
def patch_has_alliance_history_true(monkeypatch):
    async def mock_has_alliance_history(*args):
        return True

    monkeypatch.setattr(crud, crud.has_alliance_history.__name__, mock_has_alliance_history)


@pytest.fixture(scope="function")
def patch_has_alliance_history_false(monkeypatch):
    async def mock_has_alliance_history(*args):
        return False

    monkeypatch.setattr(crud, crud.has_alliance_history.__name__, mock_has_alliance_history)


@pytest.fixture(scope="function")
def patch_has_collection_true(monkeypatch):
    async def mock_has_collection(*args):
        return True

    monkeypatch.setattr(crud, crud.has_collection.__name__, mock_has_collection)


@pytest.fixture(scope="function")
def patch_has_collection_false(monkeypatch):
    async def mock_has_collection(*args):
        return False

    monkeypatch.setattr(crud, crud.has_collection.__name__, mock_has_collection)


@pytest.fixture(scope="function")
def patch_has_collection_with_timestamp_true(monkeypatch):
    async def mock_has_collection_with_timestamp(*args):
        return True

    monkeypatch.setattr(crud, crud.has_collection_with_timestamp.__name__, mock_has_collection_with_timestamp)


@pytest.fixture(scope="function")
def patch_has_collection_with_timestamp_false(monkeypatch):
    async def mock_has_collection_with_timestamp(*args):
        return False

    monkeypatch.setattr(crud, crud.has_collection_with_timestamp.__name__, mock_has_collection_with_timestamp)


@pytest.fixture(scope="function")
def patch_has_user_history_true(monkeypatch):
    async def mock_has_user_history(*args):
        return True

    monkeypatch.setattr(crud, crud.has_user_history.__name__, mock_has_user_history)


@pytest.fixture(scope="function")
def patch_has_user_history_false(monkeypatch):
    async def mock_has_user_history(*args):
        return False

    monkeypatch.setattr(crud, crud.has_user_history.__name__, mock_has_user_history)


@pytest.fixture(scope="function")
def patch_save_collection(collection_db: CollectionDB, monkeypatch):
    async def mock_save_collection(*args):
        collection_db.collection_id = 1
        return collection_db

    monkeypatch.setattr(crud, crud.save_collection.__name__, mock_save_collection)


# Dependencies


@pytest.fixture(scope="function")
def patch_root_api_key_123456():
    def override_root_api_key():
        return "123456"

    main.app.dependency_overrides[dependencies.root_api_key] = override_root_api_key
    yield
    del main.app.dependency_overrides[dependencies.root_api_key]


@pytest.fixture(scope="function")
def patch_root_api_key_Empty():
    def override_root_api_key():
        return ""

    main.app.dependency_overrides[dependencies.root_api_key] = override_root_api_key
    yield
    del main.app.dependency_overrides[dependencies.root_api_key]


@pytest.fixture(scope="function")
def patch_root_api_key_None():
    def override_root_api_key():
        return None

    main.app.dependency_overrides[dependencies.root_api_key] = override_root_api_key
    yield
    del main.app.dependency_overrides[dependencies.root_api_key]


# Helpers


@pytest.fixture(scope="function")
def assert_error_code() -> Callable[[HttpXResponse, ErrorCode], None]:
    def assert_error_code_func(response: HttpXResponse, error_code: ErrorCode):
        error = ErrorOut(**response.json())
        assert error.code == str(error_code)

    return assert_error_code_func
