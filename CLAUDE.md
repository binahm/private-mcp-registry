# CLAUDE.md

## Repository Overview

Git-based template for private MCP (Model Context Protocol) server registries. Organizations clone this to control which MCP servers their developers can install - combining curated selections from public registries with internal/private servers.

## Development Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Validate configs
python scripts/registry.py validate

# Compile registry (fetches public + merges private)
python scripts/registry.py compile

# Run tests
pytest tests/ -v

# Lint
ruff check scripts/ tests/
```

## Project Structure

```
registry.json          # Registry configuration (user-owned)
config.json            # Local settings (user-owned)
mcps/                  # Private server definitions (user-owned)
  {author}/{name}/server.json
scripts/
  registry.py          # CLI entry point
  validator.py         # Schema validation
  fetcher.py           # Public registry API client
  compiler.py          # Merge + output logic
schemas/               # JSON schemas for validation
dist/registry.json     # Compiled output
```

## Key Concepts

- **Public registries**: Fetch servers from `registry.modelcontextprotocol.io` or `api.mcp.github.com`
- **Private servers**: Local `server.json` files in `mcps/` directory
- **Compilation**: Merges public + private into single `dist/registry.json`
- **Conflict rules**: Private vs anything = error; public vs public = last wins

## RPI Workflow

This project uses the RPI (Research-Plan-Implement) workflow. See `AI_CODING.md` for details.

- `/research` - Document codebase before changes
- `/plan` - Create implementation plan
- `/implement` - Execute approved plan

## TODO Annotations

- `TODO(0)`: Critical - never merge
- `TODO(1)`: High priority - architectural flaws, major bugs
- `TODO(2)`: Medium priority - minor bugs, missing features
- `TODO(3)`: Low priority - polish, tests, documentation
- `TODO(4)`: Questions/investigations needed

## Code Style

- Python 3.12+, type hints required
- Ruff for linting (line length 100)
- BDD-style tests (Given-When-Then)
- Dataclasses for structured data
