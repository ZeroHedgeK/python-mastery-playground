.PHONY: install test test-cov lint format clean run

install:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=python_mastery --cov-report=html --cov-report=term-missing --cov-fail-under=45

lint:
	ruff check src tests
	mypy src

format:
	black src tests examples
	isort src tests examples
	ruff check --fix src tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name ".ruff_cache" -exec rm -rf {} +

run:
	python -m python_mastery
