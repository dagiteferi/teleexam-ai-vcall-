from typing import Iterator, Any


class FakeLLMPort:
    def __init__(self, fixed_response: Any = None):
        self.fixed_response = fixed_response or {"intent": "test_intent"}

    async def complete_structured(self, *args, **kwargs):
        return self.fixed_response

    async def stream(self, *args, **kwargs) -> Iterator[str]:
        yield "token1"
        yield "token2"
        yield "token3"


class FakeCachePort:
    def __init__(self):
        self.store = {}

    async def get(self, key: str):
        return self.store.get(key)

    async def set(self, key: str, value: str, ttl_seconds: int | None = None):
        self.store[key] = value

    async def delete(self, key: str):
        self.store.pop(key, None)