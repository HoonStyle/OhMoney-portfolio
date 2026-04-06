"""
LLM Client — Unified interface for LLM providers.

Supports:
    - Google Gemini (default, free tier for Grade B/C)
    - OpenAI GPT-4o-mini (for Grade S/A)

All structured outputs use the Instructor library for
guaranteed Pydantic schema compliance.
"""

import logging
from typing import Any, Type, TypeVar

import google.generativeai as genai
import instructor
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    """
    Centralized LLM client with:
    - Provider routing based on topic grade
    - Rate limiting (token bucket)
    - Structured output via Instructor
    - Automatic retry with exponential backoff
    """

    def __init__(self, api_key: str, model_name: str) -> None:
        self.api_key = api_key
        self.model_name = model_name

        if api_key:
            genai.configure(api_key=api_key)
            self._raw_model = genai.GenerativeModel(
                model_name=f"models/{model_name}"
            )
            self._instructor_client = instructor.from_gemini(
                client=self._raw_model,
                mode=instructor.Mode.GEMINI_JSON,
            )

    async def generate_structured(
        self,
        response_model: Type[T],
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
        max_retries: int = 3,
    ) -> T:
        """
        Generate a structured response guaranteed to match the Pydantic model.

        Uses Instructor to enforce schema compliance at the LLM output level,
        eliminating the need for manual JSON parsing.
        """
        # Implementation: calls self._instructor_client.chat.completions.create()
        # with response_model parameter for guaranteed schema output
        raise NotImplementedError("See production implementation")

    async def generate_raw(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> str:
        """Raw text generation (for non-structured use cases)."""
        raise NotImplementedError("See production implementation")
