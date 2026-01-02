# Private MCP Registry

A git-based template for managing private MCP (Model Context Protocol) server registries. Organizations clone this to control which MCP servers their developers can install.

## Quick Start

```bash
# Clone this template
git clone https://github.com/your-org/private-mcp-registry.git
cd private-mcp-registry

# Install dependencies
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .

# Validate configuration
python scripts/registry.py validate

# Compile registry
python scripts/registry.py compile

# Add a remote MCP server (SSE)
python scripts/registry.py add --transport sse atlassian/rovo https://mcp.atlassian.com/v1/sse

# Add a stdio MCP server (npx)
python scripts/registry.py add --transport stdio anthropic/everything -- npx -y @anthropic/mcp-server-everything
```

## Configuration

### registry.json

Define which servers to include from public registries and private sources:

```json
{
    "registries": [
        {
            "name": "MCP Official",
            "url": "https://registry.modelcontextprotocol.io",
            "servers": {
                "ai.exa/exa": "latest",
                "some-org/some-server": "1.0.0"
            }
        },
        {
            "name": "VSCode",
            "url": "https://api.mcp.github.com",
            "servers": "*",
            "exclude": ["unwanted/server"]
        },
        {
            "name": "private",
            "type": "private",
            "servers_relative_path": [
                "mcps/your-org/your-server/server.json"
            ]
        }
    ]
}
```

### config.json

Local settings for the compilation process:

```json
{
    "output": "dist/registry.json",
    "fetchTimeout": 30
}
```

## Adding a Private Server

1. Create `mcps/{author}/{name}/server.json`:

```json
{
    "server": {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json",
        "name": "your-org/your-server",
        "description": "Your server description",
        "version": "1.0.0",
        "packages": [
            {
                "registryType": "npm",
                "identifier": "@your-org/your-server",
                "version": "1.0.0",
                "transport": { "type": "stdio" }
            }
        ]
    }
}
```

2. Add to `registry.json`:

```json
{
    "registries": [
        {
            "name": "private",
            "type": "private",
            "servers_relative_path": [
                "mcps/your-org/your-server/server.json"
            ]
        }
    ]
}
```

3. Validate and compile:

```bash
python scripts/registry.py validate
python scripts/registry.py compile
```

## CLI Reference

```bash
# Validate all configuration files
python scripts/registry.py validate
python scripts/registry.py --json validate  # JSON output for CI

# Compile registry
python scripts/registry.py compile
python scripts/registry.py --quiet compile  # Errors only
python scripts/registry.py --json compile   # JSON output for CI
```

## Updating from Template

```bash
git remote add upstream https://github.com/template-org/private-mcp-registry.git
git fetch upstream
git merge upstream/main
```

## File Ownership

**You own (modify freely):**
- `registry.json`
- `config.json`
- `mcps/`
- `README.md`

**Template owns (pull updates):**
- `scripts/`
- `schemas/`
- `.github/workflows/`
