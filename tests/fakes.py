from typing import Iterator, Any

from app.agents.supervisor import IntentResult


class FakeLLMPort:
    def __init__(self, fixed_response: Any = None):
        self.fixed_response = fixed_response or IntentResult(
            intent="concept_search",
            confidence=0.9,
            key_entities=["python"],
        )

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

    async def set(
        self,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ):
        self.store[key] = value

    async def delete(self, key: str):
        self.store.pop(key, None)


class FakeEmbeddingPort:

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return [
            [0.1, 0.2, 0.3, 0.4, 0.5]
            for _ in texts
        ]


class FakeVectorSearchPort:

    async def search(
        self,
        query_embedding: list[float],
        top_k: int,
    ) -> list[str]:

        return [
            "Relevant curriculum content about data structures"
        ]