.PHONY: setup check format test demo clean-results

# Install everything a contributor needs. Dev extras include ruff, pytest, pre-commit.
setup:
	uv sync --extra dev
	uv run pre-commit install

# Lint + tests. Run this before pushing.
check:
	uv run ruff check .
	uv run ruff format --check .
	uv run pytest

# Autoformat.
format:
	uv run ruff format .
	uv run ruff check --fix .

# Just the tests.
test:
	uv run pytest

# End-to-end demo: run the starter flip-rate experiment on the tiny model.
demo:
	uv run syco run --config configs/experiments/flip_rate_tiny.yaml

# Remove everything inside results/ except the README and .gitkeep.
clean-results:
	find results -mindepth 1 -maxdepth 1 ! -name README.md ! -name .gitkeep -exec rm -rf {} +
