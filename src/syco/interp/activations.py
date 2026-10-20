"""Thin wrapper around the HF backend for pulling activations.

This exists so interpretability work can start from the same model loader
the eval harness uses, instead of each person writing their own.
"""

from __future__ import annotations

from typing import Any

from syco.models.base import Message


def extract_hidden_states(
    backend: Any,
    messages: list[Message],
    layers: list[int] | None = None,
) -> dict:
    """Return hidden states for the last prompt token.

    Only works for backends that expose `.hidden_states(...)` (currently HF).
    """
    if not hasattr(backend, "hidden_states"):
        raise TypeError(
            f"Backend {type(backend).__name__} does not support hidden_states. Use the HF backend."
        )
    return backend.hidden_states(messages, layers=layers)
