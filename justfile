default: release

format:
    uv run ruff format --check --diff

lint:
    uv run ruff check

typecheck:
    uv run mypy .

release: format lint typecheck
