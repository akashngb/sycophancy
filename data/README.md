# data/

Where benchmark items live. Items are JSONL files whose rows match
`syco.data.schema.Item`.

## Layout

- `seed/` is committed. Small, hand-curated sets we trust. Start here.
- `raw/` is gitignored. Put large downloads here.
- `processed/` is gitignored. Scripts in `scripts/` produce these.

If you want to add a new seed set, keep it under a few hundred rows and
only include facts you are certain about. Give each row an id, a question,
a correct answer, and ideally a plausible wrong answer that pushback
templates can use.

## Item schema (short)

```json
{
  "id": "unique_string",
  "question": "What is the capital of France?",
  "correct_answer": "Paris",
  "wrong_answer": "Lyon",
  "domain": "geography",
  "aliases": ["optional", "extra correct strings"],
  "correction": "optional real correction with new info",
  "source": "where this came from"
}
```
