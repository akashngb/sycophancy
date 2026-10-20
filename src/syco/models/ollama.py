"""Ollama HTTP backend. See https://ollama.com for the server."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests

from syco.models.base import Message


@dataclass
class OllamaBackend:
    model_id: str
    name: str = "ollama"
    host: str | None = None  # defaults to OLLAMA_HOST or http://localhost:11434

    def _url(self) -> str:
        return (self.host or os.environ.get("OLLAMA_HOST") or "http://localhost:11434").rstrip(
            "/"
        ) + "/api/chat"

    def generate(self, messages: list[Message], **params: Any) -> str:
        payload = {
            "model": self.model_id,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": float(params.get("temperature", 0.0)),
                "top_p": float(params.get("top_p", 1.0)),
                "num_predict": int(params.get("max_new_tokens", 128)),
            },
        }
        resp = requests.post(self._url(), json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return (data.get("message") or {}).get("content", "").strip()

    def info(self) -> dict[str, Any]:
        return {"backend": self.name, "model_id": self.model_id, "host": self._url()}
