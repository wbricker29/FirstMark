# Makefile Quick Reference Guide

## Overview

The project now includes a comprehensive Makefile system that automates common development tasks. All commands follow the pattern: `make <target>`

To see all available commands with descriptions: **`make`** or **`make help`**

---

## Quick Start

### First-Time Setup
```bash
make setup              # Complete initial environment setup
# Edit .env with your API keys
make validate           # Verify configuration
```

### Daily Development
```bash
# Terminal 1: Start the server
make server             # or: make dev

# Terminal 2: Start ngrok tunnel
make tunnel

# Or start both in background:
make dev-all            # Start server in background
make tunnel             # Run this in separate terminal
make stop-dev           # Stop background server when done
```

### Before Committing
```bash
make pre-commit         # Run format + lint + type-check
# or run individually:
make format             # Auto-format code
make lint               # Check code quality
make type-check         # Run mypy
```

### Running Tests
```bash
make test               # Full test suite with coverage
make test-fast          # Quick tests without coverage
make test-models        # Model validation tests only
make test-webhook       # Webhook tests only
make test-specific TEST=test_workflow  # Specific test file
```

---

## Common Workflows

### Pre-Demo Checklist
```bash
make pre-demo           # Runs: validate + smoke-test + checklist
```
This validates:
- Environment configuration (.env)
- Python dependencies
- Airtable schema alignment
- Model imports and basic functionality

### Code Quality Check
```bash
make check-all          # Runs: lint + type-check + test-fast
```
Fast quality gate before commits (~30-60 seconds)

### Documentation Preview
```bash
make docs-serve         # Start MkDocs server at http://127.0.0.1:8000
# Press Ctrl+C to stop
```

### Clean Up
```bash
make clean              # Remove cache files only
make clean-all          # Deep clean (cache + docs + sessions)
```

---

## All Available Targets (by Category)

### Setup & Installation
| Command | Description |
|---------|-------------|
| `make setup` | Complete initial environment setup (one-time) |
| `make setup-dev` | Setup with additional development tools |
| `make install` | Install/update dependencies only |
| `make verify-python` | Verify Python version (3.11+) |
| `make verify-deps` | Verify required packages are installed |
| `make env-check` | Alias for validate-env |

### Development
| Command | Description |
|---------|-------------|
| `make dev` | Alias for 'make server' |
| `make server` | Start AgentOS FastAPI server (foreground, port 5001) |
| `make tunnel` | Start ngrok tunnel for webhooks |
| `make dev-all` | Start server in background |
| `make stop-dev` | Stop background development server |
| `make list-routes` | List all FastAPI routes |

### Testing
| Command | Description |
|---------|-------------|
| `make test` | Run full test suite with coverage (125 tests, 75% target) |
| `make test-fast` | Run tests without coverage (quick feedback) |
| `make test-coverage` | Generate HTML coverage report |
| `make test-watch` | Run tests on file changes (requires pytest-watch) |
| `make test-specific TEST=<name>` | Run specific test file |
| `make test-models` | Run model validation tests only |
| `make test-webhook` | Run webhook endpoint tests only |
| `make smoke-test` | Run basic smoke tests |

### Code Quality
| Command | Description |
|---------|-------------|
| `make lint` | Run ruff linter (check only, no fixes) |
| `make format` | Auto-format code with ruff |
| `make type-check` | Run mypy type checker (strict mode) |
| `make check-all` | Run all quality checks (lint + type-check + quick tests) |
| `make pre-commit` | Run before committing (format + lint + type-check) |

### Documentation
| Command | Description |
|---------|-------------|
| `make docs-serve` | Preview MkDocs documentation locally |
| `make docs-build` | Build MkDocs static site (output: site/) |
| `make docs-clean` | Clean MkDocs build artifacts |

### Validation & Utilities
| Command | Description |
|---------|-------------|
| `make validate-env` | Validate .env file has required variables |
| `make validate-airtable` | Validate Airtable client schema alignment |
| `make validate` | Run all validation checks |
| `make pre-demo` | Pre-demo validation checklist |
| `make clean` | Remove Python cache files and build artifacts |
| `make clean-all` | Remove all generated files |

---

## Advanced Usage

### Custom Port
```bash
PORT=8000 make server-custom    # Start server on custom port
```

### Pattern Matching Tests
```bash
make test-pattern PATTERN=webhook   # Run tests matching "webhook"
make test-pattern PATTERN=airtable  # Run tests matching "airtable"
```

### Specific Test File
```bash
make test-specific TEST=test_models     # Run test_models*.py
make test-specific TEST=test_workflow   # Run test_workflow*.py
```

---

## Tips & Best Practices

### 1. Always run setup first
```bash
make setup      # First time only
```

### 2. Validate environment before starting work
```bash
make validate   # Check configuration
```

### 3. Run quality checks before committing
```bash
make pre-commit     # Format + lint + type-check
```

### 4. Use fast tests during development
```bash
make test-fast      # Quick feedback loop
make test           # Full coverage before commit
```

### 5. Background server for long sessions
```bash
make dev-all        # Start in background
# ... work ...
make stop-dev       # Stop when done
```

### 6. Clean regularly
```bash
make clean          # Remove cache files
```

---

## Troubleshooting

### "Command not found: make"
Make is pre-installed on macOS/Linux. On Windows, use WSL or install via chocolatey: `choco install make`

### Server won't start (port in use)
```bash
# Check if something is using port 5001
lsof -i :5001
# Kill the process or use custom port:
PORT=8000 make server-custom
```

### .env validation fails
```bash
# Copy example and edit:
cp .env.example .env
# Add your keys:
# OPENAI_API_KEY=sk-...
# AIRTABLE_API_KEY=pat...
# AIRTABLE_BASE_ID=app...
```

### Dependencies not found
```bash
make install        # Reinstall dependencies
make verify-deps    # Verify installation
```

### Tests failing
```bash
make test-models    # Test models first
make smoke-test     # Run basic smoke tests
make test-fast      # Quick test run
```

---

## Integration with Existing Workflows

### Git Workflow
```bash
# Before commit:
make pre-commit     # Format + lint + type-check
git add .
git commit -m "Your message"

# Before push:
make test           # Full test suite
git push
```

### Demo Preparation
```bash
# Run pre-demo checklist:
make pre-demo

# Manual steps (printed by pre-demo):
# 1. make server (separate terminal)
# 2. make tunnel (separate terminal)
# 3. Test webhook endpoint
# 4. Verify Airtable automation
```

### Documentation Updates
```bash
# Preview changes:
make docs-serve     # http://127.0.0.1:8000

# Build static site:
make docs-build     # Output: site/
```

---

## Color & Emoji Output

The Makefile uses color-coded output for better readability:
- **✅ Green checkmarks** - Success
- **❌ Red crosses** - Errors
- **🔍 Blue search** - Running/checking
- **🚀 Rocket** - Starting services
- **🔧 Wrench** - Setup/configuration
- **📚 Books** - Documentation
- **🧹 Broom** - Cleaning

---

## Environment Variables

The Makefile respects these environment variables:

```bash
PORT=8000           # Custom server port
NGROK_PORT=5001     # Custom ngrok tunnel port
DOCS_PORT=8000      # Custom docs server port
```

Example:
```bash
PORT=8080 make server-custom    # Start on port 8080
```

---

## Next Steps

1. **First time?** Run `make setup`
2. **Starting work?** Run `make validate` then `make dev-all`
3. **Committing?** Run `make pre-commit`
4. **Deploying?** Run `make pre-demo`
5. **Need help?** Run `make help`

---

## Questions or Issues?

- See all targets: `make help`
- Verify setup: `make validate`
- Check environment: `make validate-env`
- Run smoke tests: `make smoke-test`
- Clean and retry: `make clean-all && make setup`

Happy coding! 🚀
