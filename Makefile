# Makefile for FirstMark Talent Signal Agent
# Self-documenting Makefile - run 'make' or 'make help' to see all targets

.DEFAULT_GOAL := help

# ============================================================================
# VARIABLES
# ============================================================================

PYTHON := python3
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PYTEST := $(VENV)/bin/pytest
UV := uv
PORT := 5001
NGROK_PORT := 5001
DOCS_PORT := 8000
PACKAGE := demo
TEST_DIR := tests

# Colors for terminal output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Emojis for status
CHECK := ✅
CROSS := ❌
SEARCH := 🔍
ROCKET := 🚀
WRENCH := 🔧
BOOKS := 📚
CLEAN := 🧹

# ============================================================================
# PHONY TARGETS (non-file targets)
# ============================================================================

.PHONY: help setup setup-dev install env-check clean clean-all \
        dev server tunnel dev-all stop-dev \
        test test-fast test-coverage test-watch test-specific test-models test-webhook \
        lint format type-check check-all pre-commit \
        docs-serve docs-build docs-clean \
        validate validate-airtable validate-env smoke-test pre-demo \
        verify-python verify-deps list-routes

# ============================================================================
# HELP & DOCUMENTATION
# ============================================================================

help: ## Show this help message
	@echo "$(BLUE)FirstMark Talent Signal Agent - Development Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Setup & Installation:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(setup|install|env-check)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(dev|server|tunnel)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "test" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Code Quality:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(lint|format|type-check|check-all|pre-commit)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Documentation:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "docs" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Validation & Utilities:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(validate|verify|clean|smoke|pre-demo)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)Examples:$(NC)"
	@echo "  make setup              # First-time setup"
	@echo "  make dev-all            # Start server + tunnel in background"
	@echo "  make test               # Run full test suite"
	@echo "  make check-all          # Run all quality checks"
	@echo "  make pre-demo           # Pre-demo validation"
	@echo ""

# ============================================================================
# SETUP & INSTALLATION
# ============================================================================

setup: verify-python ## Complete initial environment setup (one-time)
	@echo "$(WRENCH) Setting up FirstMark Talent Signal Agent..."
	@echo "$(SEARCH) Checking for UV package manager..."
	@command -v $(UV) >/dev/null 2>&1 || { \
		echo "$(CROSS) UV not found. Installing..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}
	@echo "$(CHECK) UV installed"
	@echo "$(SEARCH) Installing Python dependencies..."
	@$(UV) pip install -e .
	@echo "$(CHECK) Dependencies installed"
	@if [ ! -f .env ]; then \
		echo "$(WRENCH) Creating .env from .env.example..."; \
		cp .env.example .env; \
		echo "$(YELLOW)⚠️  Please edit .env and add your API keys$(NC)"; \
	else \
		echo "$(CHECK) .env file already exists"; \
	fi
	@echo "$(SEARCH) Verifying installation..."
	@$(MAKE) verify-deps
	@echo "$(CHECK) $(GREEN)Setup complete!$(NC)"
	@echo ""
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "  1. Edit .env and add your API keys (OPENAI_API_KEY, AIRTABLE_API_KEY, AIRTABLE_BASE_ID)"
	@echo "  2. Run 'make validate-env' to verify configuration"
	@echo "  3. Run 'make dev-all' to start development environment"
	@echo ""

setup-dev: setup ## Setup with additional development tools
	@echo "$(WRENCH) Installing development dependencies..."
	@$(UV) pip install -e ".[dev]"
	@echo "$(CHECK) Development setup complete"

install: ## Install/update dependencies only
	@echo "$(SEARCH) Installing dependencies..."
	@$(UV) pip install -e .
	@echo "$(CHECK) Dependencies installed"

verify-python: ## Verify Python version (3.11+)
	@echo "$(SEARCH) Checking Python version..."
	@$(PYTHON) --version | grep -E "Python 3\.(1[1-9]|[2-9][0-9])" > /dev/null || { \
		echo "$(CROSS) $(RED)Python 3.11+ required$(NC)"; \
		exit 1; \
	}
	@echo "$(CHECK) Python version OK"

verify-deps: ## Verify required packages are installed
	@echo "$(SEARCH) Verifying package installation..."
	@$(UV) pip list | grep -E "(agno|pydantic|fastapi|pyairtable|python-dotenv)" > /dev/null || { \
		echo "$(CROSS) $(RED)Required packages not found$(NC)"; \
		exit 1; \
	}
	@echo "$(CHECK) Required packages installed"
	@$(VENV_PYTHON) -c "from demo.models import ExecutiveResearchResult, AssessmentResult; print('$(CHECK) Models loaded successfully')" 2>/dev/null || { \
		echo "$(CROSS) $(RED)Failed to load models$(NC)"; \
		exit 1; \
	}

env-check: validate-env ## Alias for validate-env

# ============================================================================
# DEVELOPMENT SERVERS
# ============================================================================

dev: server ## Alias for 'make server' (start AgentOS server in foreground)

server: verify-deps validate-env ## Start AgentOS FastAPI server (foreground, port 5001)
	@echo "$(ROCKET) Starting AgentOS server on port $(PORT)..."
	@echo "$(BLUE)OpenAPI docs will be available at: http://localhost:$(PORT)/docs$(NC)"
	@echo "$(BLUE)Press Ctrl+C to stop$(NC)"
	@echo ""
	@source $(VENV)/bin/activate && $(UV) run python $(PACKAGE)/agentos_app.py

tunnel: ## Start ngrok tunnel for webhooks (port 5001)
	@echo "$(ROCKET) Starting ngrok tunnel on port $(NGROK_PORT)..."
	@command -v ngrok >/dev/null 2>&1 || { \
		echo "$(CROSS) $(RED)ngrok not found. Install with: brew install ngrok$(NC)"; \
		exit 1; \
	}
	@echo "$(BLUE)Copy the HTTPS URL and update your Airtable webhook$(NC)"
	@echo "$(BLUE)Press Ctrl+C to stop$(NC)"
	@echo ""
	@ngrok http $(NGROK_PORT)

dev-all: ## Start server + tunnel in background (requires tmux or manual terminal splitting)
	@echo "$(ROCKET) Starting development environment..."
	@echo "$(YELLOW)Note: This will start server in background. Use 'make stop-dev' to stop.$(NC)"
	@echo ""
	@echo "$(BLUE)Starting AgentOS server...$(NC)"
	@source $(VENV)/bin/activate && $(UV) run python $(PACKAGE)/agentos_app.py > /tmp/agentos.log 2>&1 & echo $$! > /tmp/agentos.pid
	@sleep 2
	@if curl -s http://localhost:$(PORT)/healthz > /dev/null 2>&1; then \
		echo "$(CHECK) AgentOS server running (PID: $$(cat /tmp/agentos.pid))"; \
		echo "$(BLUE)Logs: tail -f /tmp/agentos.log$(NC)"; \
	else \
		echo "$(CROSS) $(RED)Failed to start server. Check /tmp/agentos.log$(NC)"; \
		exit 1; \
	fi
	@echo ""
	@echo "$(YELLOW)To start ngrok tunnel, run in a separate terminal:$(NC)"
	@echo "  make tunnel"
	@echo ""
	@echo "$(YELLOW)To stop the server:$(NC)"
	@echo "  make stop-dev"
	@echo ""

stop-dev: ## Stop background development server
	@if [ -f /tmp/agentos.pid ]; then \
		echo "$(CLEAN) Stopping AgentOS server (PID: $$(cat /tmp/agentos.pid))..."; \
		kill $$(cat /tmp/agentos.pid) 2>/dev/null || true; \
		rm /tmp/agentos.pid; \
		echo "$(CHECK) Server stopped"; \
	else \
		echo "$(YELLOW)No running server found$(NC)"; \
	fi

list-routes: verify-deps ## List all FastAPI routes
	@echo "$(SEARCH) Available API routes:"
	@$(VENV_PYTHON) -c "from demo.agentos_app import app; routes = [{'path': r.path, 'methods': list(r.methods)} for r in app.routes if hasattr(r, 'methods')]; import json; print(json.dumps(routes, indent=2))"

# ============================================================================
# TESTING
# ============================================================================

test: ## Run full test suite with coverage (125 tests, 75% target)
	@echo "$(SEARCH) Running test suite with coverage..."
	@$(VENV_PYTEST) $(TEST_DIR)/ --cov=$(PACKAGE) --cov-report=term-missing --cov-report=html -v
	@echo ""
	@echo "$(CHECK) $(GREEN)Tests complete!$(NC)"
	@echo "$(BOOKS) HTML coverage report: htmlcov/index.html"

test-fast: ## Run tests without coverage (quick feedback)
	@echo "$(SEARCH) Running quick tests..."
	@$(VENV_PYTEST) $(TEST_DIR)/ -q

test-coverage: ## Generate HTML coverage report
	@echo "$(SEARCH) Generating coverage report..."
	@$(VENV_PYTEST) $(TEST_DIR)/ --cov=$(PACKAGE) --cov-report=html --cov-report=term
	@echo "$(CHECK) Coverage report generated: htmlcov/index.html"
	@open htmlcov/index.html 2>/dev/null || echo "$(BLUE)Open htmlcov/index.html in your browser$(NC)"

test-watch: ## Run tests on file changes (requires pytest-watch)
	@echo "$(SEARCH) Starting test watcher..."
	@$(UV) pip list | grep pytest-watch > /dev/null 2>&1 || { \
		echo "$(WRENCH) Installing pytest-watch..."; \
		$(UV) pip install pytest-watch; \
	}
	@$(VENV)/bin/ptw $(TEST_DIR)/ $(PACKAGE)/ --clear

test-specific: ## Run specific test file (usage: make test-specific TEST=test_models)
	@if [ -z "$(TEST)" ]; then \
		echo "$(CROSS) $(RED)Usage: make test-specific TEST=test_models$(NC)"; \
		exit 1; \
	fi
	@echo "$(SEARCH) Running tests matching: $(TEST)"
	@$(VENV_PYTEST) $(TEST_DIR)/ -k "$(TEST)" -v

test-models: ## Run model validation tests only
	@echo "$(SEARCH) Running model validation tests..."
	@$(VENV_PYTEST) $(TEST_DIR)/test_models_validation.py -v

test-webhook: ## Run webhook endpoint tests only
	@echo "$(SEARCH) Running webhook tests..."
	@$(VENV_PYTEST) $(TEST_DIR)/test_agentos_app.py -v

# ============================================================================
# CODE QUALITY
# ============================================================================

lint: ## Run ruff linter (check only, no fixes)
	@echo "$(SEARCH) Running ruff linter..."
	@ruff check $(PACKAGE)/ $(TEST_DIR)/
	@echo "$(CHECK) Linting complete"

format: ## Auto-format code with ruff
	@echo "$(WRENCH) Formatting code..."
	@ruff format $(PACKAGE)/ $(TEST_DIR)/
	@ruff check $(PACKAGE)/ $(TEST_DIR)/ --fix
	@echo "$(CHECK) Code formatted"

type-check: ## Run mypy type checker (strict mode)
	@echo "$(SEARCH) Running mypy type checker..."
	@mypy $(PACKAGE)/ --strict || { \
		echo "$(YELLOW)⚠️  Type checking found issues (non-blocking)$(NC)"; \
	}

check-all: lint type-check test-fast ## Run all quality checks (lint + type-check + quick tests)
	@echo ""
	@echo "$(CHECK) $(GREEN)All quality checks passed!$(NC)"

pre-commit: format lint type-check ## Run before committing (format + lint + type-check)
	@echo "$(CHECK) $(GREEN)Pre-commit checks passed!$(NC)"
	@echo "$(BLUE)Ready to commit$(NC)"

# ============================================================================
# DOCUMENTATION
# ============================================================================

docs-serve: ## Preview MkDocs documentation locally (http://127.0.0.1:8000)
	@echo "$(BOOKS) Starting MkDocs server..."
	@echo "$(BLUE)Documentation will be available at: http://127.0.0.1:$(DOCS_PORT)$(NC)"
	@echo "$(BLUE)Press Ctrl+C to stop$(NC)"
	@echo ""
	@$(UV) run mkdocs serve

docs-build: ## Build MkDocs static site (output: site/)
	@echo "$(BOOKS) Building MkDocs site..."
	@$(UV) run mkdocs build
	@echo "$(CHECK) Static site built: site/index.html"

docs-clean: ## Clean MkDocs build artifacts
	@echo "$(CLEAN) Cleaning documentation build..."
	@rm -rf site/
	@echo "$(CHECK) Documentation cleaned"

# ============================================================================
# VALIDATION & SMOKE TESTS
# ============================================================================

validate-env: ## Validate .env file has required variables
	@echo "$(SEARCH) Validating environment configuration..."
	@if [ ! -f .env ]; then \
		echo "$(CROSS) $(RED).env file not found. Run 'make setup' first$(NC)"; \
		exit 1; \
	fi
	@grep -q "OPENAI_API_KEY=sk-" .env || { \
		echo "$(CROSS) $(RED)OPENAI_API_KEY not set in .env$(NC)"; \
		exit 1; \
	}
	@grep -q "AIRTABLE_API_KEY=pat" .env || { \
		echo "$(CROSS) $(RED)AIRTABLE_API_KEY not set in .env$(NC)"; \
		exit 1; \
	}
	@grep -q "AIRTABLE_BASE_ID=app" .env || { \
		echo "$(CROSS) $(RED)AIRTABLE_BASE_ID not set in .env$(NC)"; \
		exit 1; \
	}
	@echo "$(CHECK) Environment configuration valid"

validate-airtable: verify-deps validate-env ## Validate Airtable client schema alignment
	@echo "$(SEARCH) Validating Airtable schema..."
	@$(VENV_PYTHON) scripts/validate_airtable_client.py
	@echo "$(CHECK) Airtable schema validation complete"

validate: validate-env verify-deps validate-airtable ## Run all validation checks
	@echo "$(CHECK) $(GREEN)All validations passed!$(NC)"

smoke-test: validate-env verify-deps ## Run basic smoke tests (webhook + models)
	@echo "$(SEARCH) Running smoke tests..."
	@echo "$(BLUE)Testing model imports...$(NC)"
	@$(VENV_PYTHON) -c "from demo.models import ExecutiveResearchResult, AssessmentResult; print('$(CHECK) Models OK')"
	@echo "$(BLUE)Testing basic functionality...$(NC)"
	@$(VENV_PYTEST) $(TEST_DIR)/test_models_validation.py -q
	@echo "$(CHECK) $(GREEN)Smoke tests passed!$(NC)"

pre-demo: validate smoke-test ## Pre-demo validation checklist (environment + smoke tests)
	@echo ""
	@echo "$(ROCKET) $(GREEN)Pre-Demo Checklist:$(NC)"
	@echo "  $(CHECK) Environment validated"
	@echo "  $(CHECK) Dependencies verified"
	@echo "  $(CHECK) Airtable schema aligned"
	@echo "  $(CHECK) Smoke tests passed"
	@echo ""
	@echo "$(BLUE)Manual checklist:$(NC)"
	@echo "  [ ] Start server: make server (separate terminal)"
	@echo "  [ ] Start tunnel: make tunnel (separate terminal)"
	@echo "  [ ] Verify webhook: curl http://localhost:$(PORT)/healthz"
	@echo "  [ ] Test Airtable automation (change Screen status → 'Ready to Screen')"
	@echo "  [ ] Capture screenshots of workflow stages"
	@echo ""
	@echo "$(CHECK) $(GREEN)Ready for demo!$(NC)"

# ============================================================================
# UTILITIES & CLEANUP
# ============================================================================

clean: ## Remove Python cache files and build artifacts
	@echo "$(CLEAN) Cleaning cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache/ 2>/dev/null || true
	@rm -rf htmlcov/ 2>/dev/null || true
	@rm -rf .coverage 2>/dev/null || true
	@rm -rf dist/ 2>/dev/null || true
	@rm -rf build/ 2>/dev/null || true
	@echo "$(CHECK) Cache cleaned"

clean-all: clean docs-clean ## Remove all generated files (cache + docs + sessions)
	@echo "$(CLEAN) Deep cleaning..."
	@rm -rf tmp/agno_sessions.db 2>/dev/null || true
	@rm -rf /tmp/agentos.log /tmp/agentos.pid 2>/dev/null || true
	@echo "$(CHECK) Deep clean complete"

# ============================================================================
# ADVANCED TARGETS
# ============================================================================

# Example: Run tests for a specific pattern
# Usage: make test-pattern PATTERN=webhook
test-pattern: ## Run tests matching pattern (usage: make test-pattern PATTERN=webhook)
	@if [ -z "$(PATTERN)" ]; then \
		echo "$(CROSS) $(RED)Usage: make test-pattern PATTERN=webhook$(NC)"; \
		exit 1; \
	fi
	@$(VENV_PYTEST) $(TEST_DIR)/ -k "$(PATTERN)" -v

# Example: Run with custom port
# Usage: make server PORT=8000
.PHONY: server-custom
server-custom: ## Start server on custom port (usage: PORT=8000 make server-custom)
	@echo "$(ROCKET) Starting server on port $(PORT)..."
	@FASTAPI_PORT=$(PORT) source $(VENV)/bin/activate && $(UV) run python $(PACKAGE)/agentos_app.py
