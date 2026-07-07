from collections.abc import AsyncIterator

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel

from app.core.config import settings
from app.ports.llm_port import LLMPort


class GroqLLMAdapter(LLMPort):
    def __init__(
        self,
        model: str,
        max_tokens: int = 256,
        temperature: float = 0,
    ):
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=settings.groq_api_key,
        )

    async def complete_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: type[BaseModel],
    ) -> BaseModel:
        structured_llm = self.llm.with_structured_output(schema)

        result = await structured_llm.ainvoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        )

        return result

    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> AsyncIterator[str]:
        async for chunk in self.llm.astream(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        ):
            if chunk.content:
                yield chunk.content