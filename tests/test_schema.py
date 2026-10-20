from pathlib import Path

import pytest

from syco.data.schema import Item, load_items


def test_item_minimum_fields():
    item = Item(id="x", question="q?", correct_answer="a")
    assert item.id == "x"
    assert item.domain == "general"
    assert item.aliases == []


def test_item_empty_id_rejected():
    with pytest.raises(ValueError):
        Item(id="   ", question="q", correct_answer="a")


def test_load_seed_jsonl():
    path = Path(__file__).resolve().parents[1] / "data" / "seed" / "factual_v0.jsonl"
    items = load_items(path)
    assert len(items) >= 25
    for it in items.items:
        assert it.wrong_answer, f"{it.id} needs a wrong_answer for pushback"


def test_duplicate_ids_rejected(tmp_path: Path):
    f = tmp_path / "d.jsonl"
    f.write_text(
        '{"id": "a", "question": "x", "correct_answer": "y"}\n'
        '{"id": "a", "question": "x", "correct_answer": "y"}\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate"):
        load_items(f)
