import json
from datetime import datetime
from typing import Any, Callable, Optional

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from httpx import Response as HttpXResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api import main
from src.api.database import crud
from src.api.database.models import CollectionDB
from src.api.models import AllianceHistoryOut, AllianceOut, CollectionOut, CollectionWithFleetsOut, CollectionWithUsersOut, UserHistoryOut, UserOut
from src.api.models.converters import FromDB
from src.api.models.enums import ErrorCode, ParameterInterval
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


@pytest.fixture(scope="session")
def client_without_headers():
    client = TestClient(
        main.app,
    )
    yield client


@pytest.fixture(scope="function")
def collection_metadata_out_json(collection_out_without_children: CollectionOut) -> Any:
    return json.loads(collection_out_without_children.meta.model_dump_json())


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
    def mock_check_is_authenticated(api_key: str):
        assert isinstance(api_key, str)

        return True

    monkeypatch.setattr(dependencies, dependencies._check_is_authenticated.__name__, mock_check_is_authenticated)


@pytest.fixture(scope="function")
def patch_check_is_authorized_true(monkeypatch):
    def mock_check_is_authorized(request: Request, api_key: str, root_api_key: str):
        assert isinstance(request, Request)
        assert isinstance(api_key, str)
        assert not root_api_key or isinstance(root_api_key, str)

        return True

    monkeypatch.setattr(dependencies, dependencies._check_is_authorized.__name__, mock_check_is_authorized)


@pytest.fixture(scope="function")
def patch_delete_collection_true(monkeypatch):
    async def mock_delete_collection(session: AsyncSession, collection_id: int):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection_id, int)

        return True

    monkeypatch.setattr(crud, crud.delete_collection.__name__, mock_delete_collection)


@pytest.fixture(scope="function")
def patch_get_alliance_history(alliance_history_db, monkeypatch):
    async def mock_get_alliance_history(
        session: AsyncSession,
        alliance_id: int,
        include_users: bool = True,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: ParameterInterval = ParameterInterval.MONTHLY,
        desc: bool = False,
        skip: int = 0,
        take: int = 100,
    ):
        assert isinstance(session, AsyncSession)
        assert isinstance(alliance_id, int)
        assert isinstance(include_users, bool)
        assert not from_date or isinstance(from_date, datetime)
        assert not to_date or isinstance(to_date, datetime)
        assert isinstance(interval, ParameterInterval)
        assert isinstance(desc, bool)
        assert not skip or isinstance(skip, int)
        assert not take or isinstance(take, int)

        return [alliance_history_db]

    monkeypatch.setattr(crud, crud.get_alliance_history.__name__, mock_get_alliance_history)


@pytest.fixture(scope="function")
def patch_get_alliance_from_collection(alliance_history_db, monkeypatch):
    async def mock_get_alliance_from_collection(session: AsyncSession, collection_id: int, alliance_id: int):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection_id, int)
        assert isinstance(alliance_id, int)

        return alliance_history_db

    monkeypatch.setattr(crud, crud.get_alliance_from_collection.__name__, mock_get_alliance_from_collection)


@pytest.fixture(scope="function")
def patch_get_collection_none(monkeypatch):
    async def mock_get_collection(session: AsyncSession, collection_id: int, include_alliances: bool, include_users: bool):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection_id, int)
        assert isinstance(include_alliances, bool)
        assert isinstance(include_users, bool)

        return None

    monkeypatch.setattr(crud, crud.get_collection.__name__, mock_get_collection)


@pytest.fixture(scope="function")
def patch_get_collection(collection_db: CollectionDB, monkeypatch):
    async def mock_get_collection(session: AsyncSession, collection_id: int, include_alliances: bool, include_users: bool):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection_id, int)
        assert isinstance(include_alliances, bool)
        assert isinstance(include_users, bool)

        if not include_alliances:
            collection_db.alliances = []
        if not include_users:
            collection_db.users = []
        return collection_db

    monkeypatch.setattr(crud, crud.get_collection.__name__, mock_get_collection)


@pytest.fixture(scope="function")
def patch_get_collection_by_timestamp(collection_db: CollectionDB, monkeypatch):
    async def mock_get_collection_by_timestamp(session: AsyncSession, collected_at: datetime):
        assert isinstance(session, AsyncSession)
        assert isinstance(collected_at, datetime)

        return collection_db

    monkeypatch.setattr(crud, crud.get_collection_by_timestamp.__name__, mock_get_collection_by_timestamp)


@pytest.fixture(scope="function")
def patch_get_collection_by_timestamp_none(monkeypatch):
    async def mock_get_collection_by_timestamp(session: AsyncSession, collected_at: datetime):
        assert isinstance(session, AsyncSession)
        assert isinstance(collected_at, datetime)

        return None

    monkeypatch.setattr(crud, crud.get_collection_by_timestamp.__name__, mock_get_collection_by_timestamp)


@pytest.fixture(scope="function")
def patch_get_collections(collection_db, monkeypatch):
    async def mock_get_collections(
        session: AsyncSession,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: ParameterInterval = ParameterInterval.MONTHLY,
        desc: bool = False,
        skip: int = 0,
        take: int = 100,
    ):
        assert isinstance(session, AsyncSession)
        assert not from_date or isinstance(from_date, datetime)
        assert not to_date or isinstance(to_date, datetime)
        assert isinstance(interval, ParameterInterval)
        assert isinstance(desc, bool)
        assert isinstance(skip, int)
        assert isinstance(take, int)

        return [collection_db]

    monkeypatch.setattr(crud, crud.get_collections.__name__, mock_get_collections)


@pytest.fixture(scope="function")
def patch_get_top_100_from_collection(user_db, monkeypatch):
    async def mock_get_top_100_from_collection(session: AsyncSession, collection_id: int, skip: int = 0, take: int = 100):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection_id, int)
        assert isinstance(skip, int)
        assert isinstance(take, int)

        return [user_db]

    monkeypatch.setattr(crud, crud.get_top_100_from_collection.__name__, mock_get_top_100_from_collection)


@pytest.fixture(scope="function")
def patch_get_user_from_collection(user_history_db, monkeypatch):
    async def mock_get_user_from_collection(session: AsyncSession, collection_id: int, user_id: int):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection_id, int)
        assert isinstance(user_id, int)

        return user_history_db

    monkeypatch.setattr(crud, crud.get_user_from_collection.__name__, mock_get_user_from_collection)


@pytest.fixture(scope="function")
def patch_get_user_history(user_history_db, monkeypatch):
    async def mock_get_user_history(
        session: AsyncSession,
        user_id: int,
        include_alliance: bool = True,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: ParameterInterval = ParameterInterval.MONTHLY,
        desc: bool = False,
        skip: int = 0,
        take: int = 100,
    ):
        assert isinstance(session, AsyncSession)
        assert isinstance(user_id, int)
        assert isinstance(include_alliance, bool)
        assert not from_date or isinstance(from_date, datetime)
        assert not to_date or isinstance(to_date, datetime)
        assert isinstance(interval, ParameterInterval)
        assert isinstance(desc, bool)
        assert isinstance(skip, int)
        assert isinstance(take, int)

        return [user_history_db]

    monkeypatch.setattr(crud, crud.get_user_history.__name__, mock_get_user_history)


@pytest.fixture(scope="function")
def patch_has_alliance_history_true(monkeypatch):
    async def mock_has_alliance_history(session: AsyncSession, alliance_id: int):
        assert isinstance(session, AsyncSession)
        assert isinstance(alliance_id, int)

        return True

    monkeypatch.setattr(crud, crud.has_alliance_history.__name__, mock_has_alliance_history)


@pytest.fixture(scope="function")
def patch_has_alliance_history_false(monkeypatch):
    async def mock_has_alliance_history(session: AsyncSession, alliance_id: int):
        assert isinstance(session, AsyncSession)
        assert isinstance(alliance_id, int)

        return False

    monkeypatch.setattr(crud, crud.has_alliance_history.__name__, mock_has_alliance_history)


@pytest.fixture(scope="function")
def patch_has_collection_true(monkeypatch):
    async def mock_has_collection(session: AsyncSession, collection_id: int):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection_id, int)

        return True

    monkeypatch.setattr(crud, crud.has_collection.__name__, mock_has_collection)


@pytest.fixture(scope="function")
def patch_has_collection_false(monkeypatch):
    async def mock_has_collection(session: AsyncSession, collection_id: int):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection_id, int)

        return False

    monkeypatch.setattr(crud, crud.has_collection.__name__, mock_has_collection)


@pytest.fixture(scope="function")
def patch_has_collection_with_timestamp_true(monkeypatch):
    async def mock_has_collection_with_timestamp(session: AsyncSession, collected_at: datetime):
        assert isinstance(session, AsyncSession)
        assert isinstance(collected_at, datetime)

        return True

    monkeypatch.setattr(crud, crud.has_collection_with_timestamp.__name__, mock_has_collection_with_timestamp)


@pytest.fixture(scope="function")
def patch_has_collection_with_timestamp_false(monkeypatch):
    async def mock_has_collection_with_timestamp(session: AsyncSession, collected_at: datetime):
        assert isinstance(session, AsyncSession)
        assert isinstance(collected_at, datetime)

        return False

    monkeypatch.setattr(crud, crud.has_collection_with_timestamp.__name__, mock_has_collection_with_timestamp)


@pytest.fixture(scope="function")
def patch_has_user_history_true(monkeypatch):
    async def mock_has_user_history(session: AsyncSession, user_id: int):
        assert isinstance(session, AsyncSession)
        assert isinstance(user_id, int)

        return True

    monkeypatch.setattr(crud, crud.has_user_history.__name__, mock_has_user_history)


@pytest.fixture(scope="function")
def patch_has_user_history_false(monkeypatch):
    async def mock_has_user_history(session: AsyncSession, user_id: int):
        assert isinstance(session, AsyncSession)
        assert isinstance(user_id, int)

        return False

    monkeypatch.setattr(crud, crud.has_user_history.__name__, mock_has_user_history)


@pytest.fixture(scope="function")
def patch_save_collection(collection_db: CollectionDB, monkeypatch):
    async def mock_save_collection(session: AsyncSession, collection: CollectionDB, include_alliances: bool, include_users: bool):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection, CollectionDB)
        assert isinstance(include_alliances, bool)
        assert isinstance(include_users, bool)

        collection_db.collection_id = 1
        return collection_db

    monkeypatch.setattr(crud, crud.save_collection.__name__, mock_save_collection)


@pytest.fixture(scope="function")
def patch_update_collection(monkeypatch):
    async def mock_update_collection(session: AsyncSession, collection_id: int, collection: CollectionDB):
        assert isinstance(session, AsyncSession)
        assert isinstance(collection_id, int)
        assert isinstance(collection, CollectionDB)

        collection.collection_id = 1
        return collection

    monkeypatch.setattr(crud, crud.update_collection.__name__, mock_update_collection)


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
