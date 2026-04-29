.DEFAULT_GOAL := help

POETRY := ~/Library/Python/3.13/bin/poetry
ORCH := services/orchestrator
STUDIO := services/studio-web

.PHONY: help install install-orch install-studio dev-orch dev-studio adk-web test lint typecheck fmt clean

help: ## list targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-18s\033[0m %s\n",$$1,$$2}'

install: install-orch install-studio ## install all deps

install-orch: ## install Python deps via poetry
	cd $(ORCH) && $(POETRY) install

install-studio: ## install Node deps for Studio
	cd $(STUDIO) && npm install

dev-orch: ## run FastAPI + uvicorn with reload
	cd $(ORCH) && $(POETRY) run uvicorn akhada.api.main:app --reload --port 8080

dev-studio: ## run Next.js dev server
	cd $(STUDIO) && npm run dev

adk-web: ## open ADK Dev UI
	cd $(ORCH) && $(POETRY) run adk web

test: ## run pytest
	cd $(ORCH) && $(POETRY) run pytest -q

lint: ## ruff lint
	cd $(ORCH) && $(POETRY) run ruff check .

typecheck: ## mypy strict
	cd $(ORCH) && $(POETRY) run mypy --strict src

fmt: ## ruff format
	cd $(ORCH) && $(POETRY) run ruff format .

clean: ## remove caches
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache -o -name .mypy_cache -o -name .next -o -name node_modules \) -prune -exec rm -rf {} +
