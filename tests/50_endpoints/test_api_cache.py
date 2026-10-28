from datetime import datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

import src.api.response_cache as response_cache_module
from src.api.database import crud
from src.api.database.models import CollectionDB
from src.api.models import CollectionCreate9
from src.api.models.enums import ParameterInterval
from src.api.response_cache import InMemoryResponseCache


def test_get_collection_list_is_cached(collection_db: CollectionDB, monkeypatch: pytest.MonkeyPatch, client: TestClient):
    calls = 0

    async def mock_get_collections(
        session: AsyncSession,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        interval: ParameterInterval = ParameterInterval.MONTHLY,
        desc: bool = False,
        skip: int = 0,
        take: int = 100,
    ) -> list[CollectionDB]:
        nonlocal calls
        calls += 1
        return [collection_db]

    monkeypatch.setattr(crud, crud.get_collections.__name__, mock_get_collections)
    path = f"/collections/?cache_test={uuid4()}"

    with client:
        first = client.get(path)
        second = client.get(path)

    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()
    assert first.headers["cache-control"] == "private, no-cache"
    assert second.headers["cache-control"] == "private, no-cache"
    assert first.headers["x-cache"] == "MISS"
    assert second.headers["x-cache"] == "HIT"
    assert calls == 1


@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true")
def test_successful_post_invalidates_cached_get(
    collection_db: CollectionDB,
    collection_create_9: CollectionCreate9,
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
):
    calls = 0
    collections = [collection_db]

    async def mock_get_collections(
        session: AsyncSession,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        interval: ParameterInterval = ParameterInterval.MONTHLY,
        desc: bool = False,
        skip: int = 0,
        take: int = 100,
    ) -> list[CollectionDB]:
        nonlocal calls
        calls += 1
        return collections

    async def mock_get_collection_by_timestamp(session: AsyncSession, collected_at: datetime) -> None:
        return None

    async def mock_save_collection(session: AsyncSession, collection: CollectionDB, include_alliances: bool, include_users: bool) -> CollectionDB:
        collection.collection_id = 2
        collections[:] = [collection]
        return collection

    monkeypatch.setattr(crud, crud.get_collections.__name__, mock_get_collections)
    monkeypatch.setattr(crud, crud.get_collection_by_timestamp.__name__, mock_get_collection_by_timestamp)
    monkeypatch.setattr(crud, crud.save_collection.__name__, mock_save_collection)
    path = f"/collections/?cache_test={uuid4()}"

    with client:
        before = client.get(path)
        post = client.post("/collections", content=collection_create_9.model_dump_json())
        after = client.get(path)

    assert before.status_code == after.status_code == 200
    assert post.status_code == 201
    assert before.json() != after.json()
    assert before.headers["cache-control"] == "private, no-cache"
    assert after.headers["cache-control"] == "private, no-cache"
    assert before.headers["x-cache"] == "MISS"
    assert after.headers["x-cache"] == "MISS"
    assert calls == 2


def test_response_cache_entries_expire_after_one_hour(monkeypatch: pytest.MonkeyPatch):
    now = 0.0
    monkeypatch.setattr(response_cache_module, "monotonic", lambda: now)
    cache = InMemoryResponseCache()
    key = (b"/collections/", b"", b"", b"")
    messages = ({"type": "http.response.start", "status": 200, "headers": []},)

    cache.store(key, messages, 1, cache.generation())
    now = 3599
    assert cache.get(key) == messages
    now = 3600
    assert cache.get(key) is None


@pytest.mark.usefixtures("patch_check_is_authenticated_true", "patch_check_is_authorized_true", "patch_get_collection_by_timestamp")
def test_failed_post_does_not_invalidate_cached_get(
    collection_db: CollectionDB,
    collection_create_9: CollectionCreate9,
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
):
    calls = 0

    async def mock_get_collections(
        session: AsyncSession,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        interval: ParameterInterval = ParameterInterval.MONTHLY,
        desc: bool = False,
        skip: int = 0,
        take: int = 100,
    ) -> list[CollectionDB]:
        nonlocal calls
        calls += 1
        return [collection_db]

    monkeypatch.setattr(crud, crud.get_collections.__name__, mock_get_collections)
    path = f"/collections/?cache_test={uuid4()}"

    with client:
        before = client.get(path)
        post = client.post("/collections", content=collection_create_9.model_dump_json())
        after = client.get(path)

    assert before.status_code == after.status_code == 200
    assert post.status_code == 409
    assert before.json() == after.json()
    assert before.headers["x-cache"] == "MISS"
    assert after.headers["x-cache"] == "HIT"
    assert calls == 1
