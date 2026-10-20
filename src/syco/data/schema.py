"""Pydantic schema for benchmark items.

An Item is one test case. The eval harness asks `question`, checks the
answer against `correct_answer`, then applies pushback (optionally using
`wrong_answer`). If `correction` is set, that item is also used to test
whether the model accepts a real correction instead of only resisting one.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from syco.utils.io import load_jsonl


class Item(BaseModel):
    id: str
    question: str
    correct_answer: str
    domain: str = Field(default="general")
    source: str | None = None
    # Used by pushback templates that want to assert a specific wrong value.
    # If missing, pushback that needs it will skip the item.
    wrong_answer: str | None = None
    # A real correction, with new information. Used to measure correction
    # acceptance rate. If set, this item is answered under the premise that
    # the model's first answer is actually wrong.
    correction: str | None = None
    # Optional list of extra accepted strings (synonyms, alt capitalization).
    aliases: list[str] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("id must be non-empty")
        return v


class ItemSet(BaseModel):
    items: list[Item]

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):  # type: ignore[override]
        return iter(self.items)


def load_items(path: Path | str) -> ItemSet:
    """Load and validate a JSONL file of items."""
    rows = load_jsonl(path)
    items = [Item.model_validate(r) for r in rows]
    # Enforce unique ids within a file.
    ids = [i.id for i in items]
    dupes = {x for x in ids if ids.count(x) > 1}
    if dupes:
        raise ValueError(f"duplicate ids in {path}: {sorted(dupes)}")
    return ItemSet(items=items)
