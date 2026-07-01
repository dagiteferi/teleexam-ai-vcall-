from collections.abc import AsyncIterator
from typing import Protocol
from pydantic import BaseModel


class LLMPort(Protocol):
    async def complete_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: type[BaseModel],
    ) -> BaseModel:
        ...

    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> AsyncIterator[str]:
        ...