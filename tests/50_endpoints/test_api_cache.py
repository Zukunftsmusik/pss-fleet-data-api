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
from src.api.response_cache import InMemoryResponseCache, ResponseCacheMiddleware


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


def test_cache_does_not_store_oversized_or_invalidated_entries():
    cache = InMemoryResponseCache(max_entry_bytes=3)
    key = (b"/collections/", b"", b"", b"")
    messages = ({"type": "http.response.start", "status": 200, "headers": []},)

    cache.store(key, messages, 4, cache.generation())
    assert cache.get(key) is None

    generation = cache.generation()
    cache.invalidate()
    cache.store(key, messages, 1, generation)
    assert cache.get(key) is None


def test_replacing_cache_entry_releases_previous_size():
    cache = InMemoryResponseCache(max_size_bytes=5)
    first_key = (b"/collections/1", b"", b"", b"")
    second_key = (b"/collections/2", b"", b"", b"")
    old_messages = ({"type": "http.response.start", "status": 200, "headers": [(b"x-value", b"old")]},)
    new_messages = ({"type": "http.response.start", "status": 200, "headers": [(b"x-value", b"new")]},)
    generation = cache.generation()

    cache.store(first_key, old_messages, 2, generation)
    cache.store(first_key, new_messages, 3, generation)
    cache.store(second_key, old_messages, 2, generation)

    assert cache.get(first_key) == new_messages
    assert cache.get(second_key) == old_messages


def test_cache_evicts_least_recently_used_entry_when_full():
    cache = InMemoryResponseCache(max_size_bytes=2)
    first_key = (b"/collections/1", b"", b"", b"")
    second_key = (b"/collections/2", b"", b"", b"")
    third_key = (b"/collections/3", b"", b"", b"")
    messages = ({"type": "http.response.start", "status": 200, "headers": []},)
    generation = cache.generation()

    cache.store(first_key, messages, 1, generation)
    cache.store(second_key, messages, 1, generation)
    assert cache.get(first_key) == messages
    cache.store(third_key, messages, 1, generation)

    assert cache.get(first_key) == messages
    assert cache.get(second_key) is None
    assert cache.get(third_key) == messages


def test_authorized_and_cookie_requests_bypass_response_cache(collection_db: CollectionDB, monkeypatch: pytest.MonkeyPatch, client: TestClient):
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

    with client:
        authorized_responses = [client.get("/collections/?cache_test=authorized", headers={"Authorization": "test-key"}) for _ in range(2)]
        cookie_responses = [client.get("/collections/?cache_test=cookie", headers={"Cookie": "session=test"}) for _ in range(2)]

    assert all(response.status_code == 200 for response in authorized_responses + cookie_responses)
    assert all("x-cache" not in response.headers for response in authorized_responses + cookie_responses)
    assert calls == 4


async def test_oversized_streamed_response_is_returned_and_not_cached():
    calls = 0
    response_messages = [
        {"type": "http.response.start", "status": 200, "headers": []},
        {"type": "http.response.body", "body": b"ab", "more_body": True},
        {"type": "http.response.body", "body": b"cd", "more_body": True},
        {"type": "http.response.body", "body": b"ef", "more_body": False},
        {"type": "http.response.trailers", "headers": [(b"x-trailer", b"preserved")], "more_trailers": False},
    ]

    async def app(scope, receive, send):
        nonlocal calls
        calls += 1
        for message in response_messages:
            await send(message)

    middleware = ResponseCacheMiddleware(app, InMemoryResponseCache(max_entry_bytes=3))
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/collections/",
        "query_string": b"",
        "headers": [],
        "extensions": {"http.response.trailers": {}},
    }

    async def make_request():
        sent_messages = []

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message):
            sent_messages.append(message)

        await middleware(scope, receive, send)
        return sent_messages

    first_response = await make_request()
    second_response = await make_request()

    assert b"".join(message.get("body", b"") for message in first_response) == b"abcdef"
    assert b"".join(message.get("body", b"") for message in second_response) == b"abcdef"
    assert dict(first_response[0]["headers"])[b"x-cache"] == b"BYPASS"
    assert dict(second_response[0]["headers"])[b"x-cache"] == b"BYPASS"
    assert first_response[-1] == response_messages[-1]
    assert second_response[-1] == response_messages[-1]
    assert calls == 2


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
