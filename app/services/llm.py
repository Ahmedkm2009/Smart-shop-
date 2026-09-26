"""OpenAI-compatible client pointed at FreeLLMAPI (or any compatible gateway)."""

from typing import Any, cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from app.config import settings


def get_llm_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=settings.openai_api_key or "dummy",
        base_url=settings.openai_base_url,
    )


async def chat(messages: list[dict[str, Any]], model: str | None = None) -> str:
    """Simple chat helper. Returns the assistant message content."""
    client = get_llm_client()
    response = await client.chat.completions.create(
        model=model or settings.llm_model,
        messages=cast(list[ChatCompletionMessageParam], messages),
        temperature=0.7,
    )
    return response.choices[0].message.content or ""
