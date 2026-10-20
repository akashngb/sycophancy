"""OpenAI-compatible chat completions backend.

Works with vLLM's OpenAI server, LM Studio, llama.cpp server with the
OpenAI shim, and the real OpenAI API. The base URL and model id come
from the model config; the API key is read from the env var named in
`api_key_env` (default OPENAI_API_KEY). An empty/missing key is fine
for local servers that don't require auth.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests

from syco.models.base import Message


@dataclass
class OpenAICompatBackend:
    model_id: str
    name: str = "openai_compat"
    base_url: str | None = None
    api_key_env: str = "OPENAI_API_KEY"

    def _url(self) -> str:
        base = (
            self.base_url
            or os.environ.get("OPENAI_COMPATIBLE_BASE_URL")
            or "http://localhost:8000/v1"
        )
        return base.rstrip("/") + "/chat/completions"

    def _headers(self) -> dict[str, str]:
        h = {"Content-Type": "application/json"}
        key = os.environ.get(self.api_key_env, "")
        if key:
            h["Authorization"] = f"Bearer {key}"
        return h

    def generate(self, messages: list[Message], **params: Any) -> str:
        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": float(params.get("temperature", 0.0)),
            "top_p": float(params.get("top_p", 1.0)),
            "max_tokens": int(params.get("max_new_tokens", 128)),
            "stream": False,
        }
        resp = requests.post(self._url(), json=payload, headers=self._headers(), timeout=120)
        resp.raise_for_status()
        data = resp.json()
        choices = data.get("choices") or []
        if not choices:
            return ""
        return (choices[0].get("message") or {}).get("content", "").strip()

    def info(self) -> dict[str, Any]:
        return {"backend": self.name, "model_id": self.model_id, "base_url": self._url()}
