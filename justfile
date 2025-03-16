default: release

format:
    uv run ruff format --check

lint:
    uv run ruff check

typecheck:
    uv run mypy .

release: format lint typecheck
