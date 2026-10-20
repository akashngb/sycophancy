"""Build a backend from a model config dict.

Config shape (YAML):
    name: a short label (used in results dirs)
    backend: hf | ollama | openai_compat | openai_api | anthropic | fake
    model_id: the id the backend expects
    # backend-specific overrides, all optional:
    device: auto | cpu | mps | cuda
    dtype: auto | float16 | bfloat16 | float32
    trust_remote_code: false
    base_url: ...
    host: ...
    api_key_env: OPENAI_API_KEY
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from syco.models.base import Backend


def load_model_config(path: Path | str) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if "backend" not in cfg or "model_id" not in cfg:
        raise ValueError(f"{path}: model config needs 'backend' and 'model_id'")
    cfg.setdefault("name", Path(path).stem)
    return cfg


def build_backend(cfg: dict[str, Any]) -> Backend:
    backend = cfg["backend"]
    model_id = cfg["model_id"]
    if backend == "hf":
        from syco.models.hf import HFBackend

        return HFBackend(
            model_id=model_id,
            device=cfg.get("device"),
            dtype=cfg.get("dtype", "auto"),
            trust_remote_code=bool(cfg.get("trust_remote_code", False)),
        )
    if backend == "ollama":
        from syco.models.ollama import OllamaBackend

        return OllamaBackend(model_id=model_id, host=cfg.get("host"))
    if backend == "openai_compat":
        from syco.models.openai_compat import OpenAICompatBackend

        return OpenAICompatBackend(
            model_id=model_id,
            base_url=cfg.get("base_url"),
            api_key_env=cfg.get("api_key_env", "OPENAI_API_KEY"),
        )
    if backend == "openai_api":
        from syco.models.openai_api import OpenAIBackend

        return OpenAIBackend(model_id=model_id)
    if backend == "anthropic":
        from syco.models.anthropic_api import AnthropicBackend

        return AnthropicBackend(model_id=model_id)
    if backend == "fake":
        from syco.models.fake import FakeBackend

        return FakeBackend(
            model_id=model_id,
            rules=dict(cfg.get("rules") or {}),
            caves=bool(cfg.get("caves", False)),
            cave_text=cfg.get("cave_text", "You're right, I was wrong."),
            default=cfg.get("default", "I don't know."),
        )
    raise ValueError(f"unknown backend {backend!r}")
