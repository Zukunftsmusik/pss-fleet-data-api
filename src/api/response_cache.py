from collections import OrderedDict
from threading import RLock
from time import monotonic

from starlette.types import ASGIApp, Message, Receive, Scope, Send


class InMemoryResponseCache:
    """A bounded, process-local cache for successful API GET responses."""

    def __init__(
        self,
        ttl_seconds: int = 3600,
        max_size_bytes: int = 64 * 1024 * 1024,
        max_entry_bytes: int = 8 * 1024 * 1024,
        max_entries: int = 512,
    ):
        self.ttl_seconds = ttl_seconds
        self.max_size_bytes = max_size_bytes
        self.max_entry_bytes = max_entry_bytes
        self.max_entries = max_entries
        self._entries: OrderedDict[tuple[bytes, ...], tuple[float, tuple[Message, ...], int]] = OrderedDict()
        self._size_bytes = 0
        self._generation = 0
        self._lock = RLock()

    def get(self, key: tuple[bytes, ...]) -> tuple[Message, ...] | None:
        with self._lock:
            cached = self._entries.get(key)
            if cached is None:
                return None

            expires_at, messages, size_bytes = cached
            if expires_at <= monotonic():
                del self._entries[key]
                self._size_bytes -= size_bytes
                return None

            self._entries.move_to_end(key)
            return messages

    def store(self, key: tuple[bytes, ...], messages: tuple[Message, ...], size_bytes: int, generation: int) -> None:
        if size_bytes > self.max_entry_bytes:
            return

        with self._lock:
            if generation != self._generation:
                return

            previous = self._entries.pop(key, None)
            if previous is not None:
                self._size_bytes -= previous[2]

            while self._entries and (self._size_bytes + size_bytes > self.max_size_bytes or len(self._entries) >= self.max_entries):
                _, (_, _, removed_size) = self._entries.popitem(last=False)
                self._size_bytes -= removed_size

            if size_bytes <= self.max_size_bytes:
                self._entries[key] = (monotonic() + self.ttl_seconds, messages, size_bytes)
                self._size_bytes += size_bytes

    def generation(self) -> int:
        with self._lock:
            return self._generation

    def invalidate(self) -> None:
        with self._lock:
            self._entries.clear()
            self._size_bytes = 0
            self._generation += 1


class ResponseCacheMiddleware:
    """Caches compressed API responses in memory and invalidates after successful writes."""

    _mutating_methods = {b"POST", b"PUT", b"PATCH", b"DELETE"}
    _cacheable_prefixes = ("/collections", "/alliances", "/users")
    _cache_control = b"private, no-cache"

    def __init__(self, app: ASGIApp, cache: InMemoryResponseCache):
        self.app = app
        self.cache = cache

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope["method"].encode("ascii")
        if method in self._mutating_methods:
            await self._process_write(scope, receive, send)
            return

        key = self._cache_key(scope, method)
        if key is None:
            await self.app(scope, receive, send)
            return

        cached_messages = self.cache.get(key)
        if cached_messages is not None:
            await self._send_cached(cached_messages, send)
            return

        generation = self.cache.generation()
        capture = _ResponseCapture(self._cache_control, self.cache.max_entry_bytes, send)
        await self.app(scope, receive, capture)

        if capture.status_code == 200 and capture.cacheable and capture.messages:
            cached_messages = tuple(dict(message) for message in capture.messages)
            self.cache.store(key, cached_messages, capture.size_bytes, generation)

        for message in capture.messages:
            await send(message)

    async def _process_write(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def track_response(message: Message) -> None:
            if message["type"] == "http.response.start" and 200 <= message["status"] < 300:
                self.cache.invalidate()
            await send(message)

        await self.app(scope, receive, track_response)

    def _cache_key(self, scope: Scope, method: bytes) -> tuple[bytes, ...] | None:
        path = scope["path"]
        if method != b"GET" or not any(path == prefix or path.startswith(f"{prefix}/") for prefix in self._cacheable_prefixes):
            return None

        headers = {name.lower(): value for name, value in scope["headers"]}
        if headers.get(b"authorization") or headers.get(b"cookie"):
            return None

        return (
            path.encode("utf-8"),
            scope["query_string"],
            headers.get(b"accept", b""),
            headers.get(b"accept-encoding", b""),
        )

    async def _send_cached(self, messages: tuple[Message, ...], send: Send) -> None:
        for message in messages:
            if message["type"] == "http.response.start":
                message = dict(message)
                message["headers"] = self._set_header(message["headers"], b"x-cache", b"HIT")
            await send(message)

    @staticmethod
    def _set_header(headers: list[tuple[bytes, bytes]], name: bytes, value: bytes) -> list[tuple[bytes, bytes]]:
        return [(header_name, header_value) for header_name, header_value in headers if header_name.lower() != name] + [(name, value)]


class _ResponseCapture:
    def __init__(self, cache_control: bytes, max_entry_bytes: int, send: Send):
        self.cache_control = cache_control
        self.max_entry_bytes = max_entry_bytes
        self.send = send
        self.messages: list[Message] = []
        self.size_bytes = 0
        self.cacheable = True
        self.status_code: int | None = None

    async def __call__(self, message: Message) -> None:
        if message["type"] == "http.response.start":
            await self._capture_start(message)
        else:
            await self._capture_body(message)

    async def _capture_start(self, message: Message) -> None:
        self.status_code = message["status"]
        if self.status_code != 200:
            self.cacheable = False
            await self.send(message)
            return

        message = dict(message)
        headers = ResponseCacheMiddleware._set_header(message["headers"], b"cache-control", self.cache_control)
        message["headers"] = ResponseCacheMiddleware._set_header(headers, b"x-cache", b"MISS")
        self.messages.append(message)

    async def _capture_body(self, message: Message) -> None:
        if self.status_code != 200:
            await self.send(message)
            return

        if message["type"] == "http.response.body":
            self.size_bytes += len(message.get("body", b""))
            if self.size_bytes > self.max_entry_bytes:
                await self._bypass(message)
                return

        if self.cacheable:
            self.messages.append(message)
        else:
            await self.send(message)

    async def _bypass(self, message: Message) -> None:
        self.cacheable = False
        if self.messages:
            start_message = dict(self.messages[0])
            start_message["headers"] = ResponseCacheMiddleware._set_header(start_message["headers"], b"x-cache", b"BYPASS")
            self.messages[0] = start_message
            for buffered_message in self.messages:
                await self.send(buffered_message)
            self.messages.clear()
        await self.send(message)


RESPONSE_CACHE = InMemoryResponseCache()
