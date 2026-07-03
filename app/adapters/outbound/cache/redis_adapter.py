from redis.asyncio import Redis


class RedisAdapter:
    def __init__(self, host: str, port: int = 6379):
        self._redis = Redis(host=host, port=port, decode_responses=True)

    async def get(self, key: str) -> str | None:
        value = await self._redis.get(key)
        return value  # already str because decode_responses=True

    async def set(self, key: str, value: str, ttl_seconds: int | None = None) -> None:
        if ttl_seconds is not None:
            await self._redis.set(name=key, value=value, ex=ttl_seconds)
        else:
            await self._redis.set(name=key, value=value)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)