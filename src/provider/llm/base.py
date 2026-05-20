from typing import Any, Optional, cast
from utils.config import LLMConfig
from litellm import acompletion, Choices
from litellm.types.completion import ChatCompletionMessageParam as Message


class LLMProvider:
    def __init__(
        self,
        model: str,
        api_key: str,
        api_base: Optional[str],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs: Any,
    ):
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._settings = kwargs

    @classmethod
    def from_config(cls, llm: LLMConfig) -> "LLMProvider":
        return cls(
            model=llm.model,
            api_key=llm.api_key,
            api_base=llm.api_base_url,
            max_tokens=llm.max_tokens,
            temperature=llm.temperature,
        )

    async def chat(self, messages: list[Message], **kwargs: Any) -> str:
        kwargs_request = {
            "model": self.model,
            "messages": messages,
            "api_key": self.api_key,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if self.api_base:
            kwargs_request["api_base"] = self.api_base
        kwargs_request.update(kwargs)

        response = await acompletion(**kwargs_request)
        message = cast(Choices, response.choices[0]).message
        return message.content or ""
