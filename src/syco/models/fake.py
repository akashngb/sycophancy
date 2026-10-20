"""Deterministic fake backend used in tests and quick sanity checks.

Does not import torch or transformers. Behavior is driven by a dict of
{query_fragment -> response} rules, with an optional "cave" flag that
causes the backend to switch to the wrong answer after the first turn.
This is enough to drive the eval harness without any model downloads.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from syco.models.base import Message


@dataclass
class FakeBackend:
    name: str = "fake"
    model_id: str = "fake-local"
    # Map: substring in the latest user turn -> fixed response.
    rules: dict[str, str] = field(default_factory=dict)
    # If True, after seeing any assistant turn in history, the next
    # response flips to a cave response. If the latest user turn contains
    # "it's X" (as the pressure templates do), the fake backend echoes X
    # so the checker can register it as the wrong answer.
    caves: bool = False
    cave_text: str = "You're right, I was wrong."
    default: str = "I don't know."

    _IT_IS_RE: Any = field(
        default=re.compile(r"it'?s\s+([A-Za-z0-9][^.?!,\n]*)", re.IGNORECASE),
        init=False,
        repr=False,
    )

    def generate(self, messages: list[Message], **params: Any) -> str:
        # Count prior assistant turns to decide caving behavior.
        assistant_turns = sum(1 for m in messages if m["role"] == "assistant")
        latest_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )

        if self.caves and assistant_turns >= 1:
            m = self._IT_IS_RE.search(latest_user)
            if m:
                claim = m.group(1).strip().rstrip(".?!,")
                return f"You're right, it's {claim}."
            return self.cave_text

        for key, resp in self.rules.items():
            if key.lower() in latest_user.lower():
                return resp
        return self.default

    def info(self) -> dict[str, Any]:
        return {
            "backend": self.name,
            "model_id": self.model_id,
            "caves": self.caves,
            "rule_count": len(self.rules),
        }
