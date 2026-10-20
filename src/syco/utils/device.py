from __future__ import annotations

import os


def pick_device(override: str | None = None) -> str:
    """Pick the best torch device, with manual override.

    Order: explicit arg > SYCO_DEVICE env var > CUDA > MPS > CPU.
    Returns a string ("cuda", "mps", or "cpu") so callers don't need
    to depend on torch at import time.
    """
    choice = (override or os.environ.get("SYCO_DEVICE") or "auto").lower()
    if choice in {"cuda", "mps", "cpu"}:
        return choice

    try:
        import torch
    except ImportError:
        return "cpu"

    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
        return "mps"
    return "cpu"
