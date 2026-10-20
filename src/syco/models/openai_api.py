"""OpenAI API backend. Requires the "api" extra and OPENAI_API_KEY.

For local OpenAI-compatible servers (vLLM, LM Studio) use the
openai_compat backend instead; this one talks to api.openai.com.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from syco.models.base import Message


@dataclass
class OpenAIBackend:
    model_id: str
    name: str = "openai_api"

    def generate(self, messages: list[Message], **params: Any) -> str:
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "The 'openai' package is not installed. Install the api extra: uv sync --extra api"
            ) from e

        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

        client = OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=float(params.get("temperature", 0.0)),
            top_p=float(params.get("top_p", 1.0)),
            max_tokens=int(params.get("max_new_tokens", 128)),
        )
        return (resp.choices[0].message.content or "").strip()

    def info(self) -> dict[str, Any]:
        return {"backend": self.name, "model_id": self.model_id}
