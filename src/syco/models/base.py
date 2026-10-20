"""Backend interface shared by every model implementation.

A Backend takes a list of chat messages (OpenAI-style dicts) and returns
a string. Keep the interface small so new backends are easy to add.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, TypedDict


class Message(TypedDict):
    role: str  # "system", "user", or "assistant"
    content: str


@dataclass
class GenerationParams:
    max_new_tokens: int = 128
    temperature: float = 0.0  # greedy by default for reproducibility
    top_p: float = 1.0
    stop: list[str] = field(default_factory=list)
    seed: int | None = 0


class Backend(Protocol):
    name: str
    model_id: str

    def generate(self, messages: list[Message], **params: Any) -> str: ...

    def info(self) -> dict[str, Any]: ...
