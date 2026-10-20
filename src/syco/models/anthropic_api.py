"""Anthropic API backend. Requires the "api" extra and ANTHROPIC_API_KEY."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from syco.models.base import Message


@dataclass
class AnthropicBackend:
    model_id: str
    name: str = "anthropic"

    def generate(self, messages: list[Message], **params: Any) -> str:
        try:
            import anthropic
        except ImportError as e:
            raise ImportError(
                "The 'anthropic' package is not installed. "
                "Install the api extra: uv sync --extra api"
            ) from e

        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set.")

        client = anthropic.Anthropic(api_key=key)
        system_parts = [m["content"] for m in messages if m["role"] == "system"]
        chat = [m for m in messages if m["role"] != "system"]
        resp = client.messages.create(
            model=self.model_id,
            system="\n".join(system_parts) if system_parts else anthropic.NOT_GIVEN,
            messages=chat,
            max_tokens=int(params.get("max_new_tokens", 256)),
            temperature=float(params.get("temperature", 0.0)),
        )
        parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
        return "".join(parts).strip()

    def info(self) -> dict[str, Any]:
        return {"backend": self.name, "model_id": self.model_id}
