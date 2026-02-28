# API Intelligence MCP Server

[![Python 3.12+](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![MCP](https://img.shields.io/badge/MCP-Enabled-green.svg)](https://modelcontextprotocol.io)

🤖 **MCP server for intelligent API workflows: analyze responses, optimize schemas, generate docs, and compare versions with AI**

Built during **DevConf Pune 2025** using Model Context Protocol (MCP) and FastMCP framework.

## Description

An MCP server that enables AI assistants to intelligently streamline API development workflows. Instead of manually debugging API responses, writing documentation, or comparing versions, this server provides four powerful tools that AI can orchestrate contextually.

## Features

### 🔍 API Response Analyzer
Intelligent parsing and validation of API responses with:
- Structured field inventory and type detection
- Null field and empty array detection
- Payload size analysis
- Nesting depth calculation
- Optimization suggestions
- Human-readable summary generation

### ⚡ API Schema Optimizer
Automated schema optimization with:
- Null field removal
- Empty array cleanup
- Size reduction metrics
- Before/after comparison
- Configurable optimization rules

### 📝 API Documentation Generator
Context-aware API documentation generation:
- Automatic endpoint documentation
- Request/response examples
- Field descriptions
- Type information
- Usage examples

### 🔄 API Response Comparator
Smart diff analysis across API versions:
- Field-level comparison
- Type change detection
- Added/removed field tracking
- Breaking change identification
- Version migration guidance

## Why MCP?

Traditional API tools require explicit integration and manual invocation. With MCP:
- AI discovers tools dynamically
- AI decides when and how to use them
- Context flows naturally between model and tools
- Multi-step reasoning becomes possible

It's the difference between "calling an API" and "enabling AI to orchestrate capabilities intelligently."

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (fast Python package installer)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/api-intelligence-mcp
cd api-intelligence-mcp

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Configure environment
cp .env.example .env

# Run the server
api-intelligence-mcp
```

### Verify Installation

```bash
# Health check
curl http://localhost:3000/health

# Test analyze tool
curl -X POST "http://localhost:3000/mcp" \
     -H "Content-Type: application/json" \
     -d '{
       "method": "tools/call",
       "params": {
         "name": "analyze_api_response",
         "arguments": {
           "response_json": "{\"id\": 1, \"name\": \"John\", \"email\": null}"
         }
       }
     }'
```

## Usage Examples

### Analyze API Response

```python
# Input: API response JSON
{
  "id": 1,
  "name": "John Doe",
  "email": null,
  "tags": [],
  "metadata": {
    "created": "2025-01-01",
    "updated": null
  }
}

# Output: Structured analysis
{
  "field_count": 6,
  "null_fields": ["email", "metadata.updated"],
  "empty_arrays": ["tags"],
  "payload_size_kb": 0.12,
  "max_nesting_depth": 2,
  "suggestions": [
    "Avoid returning null values",
    "Avoid returning empty arrays where possible"
  ]
}
```

### Optimize Schema

```python
# Removes null fields and empty arrays
# Original: 0.12 KB → Optimized: 0.08 KB
# Size reduction: 33%
```

### Generate Documentation

```python
# Automatically generates:
# - Endpoint description
# - Request/response schemas
# - Field documentation
# - Usage examples
```

### Compare API Versions

```python
# Detects:
# - Added fields
# - Removed fields
# - Type changes
# - Breaking changes
```

## Configuration

Environment variables (`.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_HOST` | `0.0.0.0` | Server bind address |
| `MCP_PORT` | `3000` | Server port |
| `MCP_TRANSPORT_PROTOCOL` | `streamable-http` | Transport protocol |
| `PYTHON_LOG_LEVEL` | `INFO` | Logging level |

## Architecture

```
api-intelligence-mcp/
├── template_mcp_server/
│   ├── src/
│   │   ├── main.py              # Application entry point
│   │   ├── api.py               # FastAPI application
│   │   ├── mcp.py               # MCP server & tool registration
│   │   ├── settings.py          # Configuration management
│   │   └── tools/               # API intelligence tools
│   │       ├── analyze_api_response.py
│   │       ├── optimize_api_response_schema.py
│   │       ├── generate_api_documentation.py
│   │       └── compare_api_responses.py
│   └── utils/
│       └── pylogger.py          # Structured logging
├── tests/                       # Test suite
├── pyproject.toml              # Project metadata
└── README.md
```

## Development

### Run Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=template_mcp_server
```

### Code Quality

```bash
# Linting
ruff check .

# Formatting
ruff format .

# Type checking
mypy template_mcp_server/
```

## Container Deployment

### Using Docker/Podman

```bash
# Build
podman build -t api-intelligence-mcp .

# Run
podman run -p 3000:3000 --env-file .env api-intelligence-mcp
```

### Using Compose

```bash
podman-compose up --build
```

## Use Cases

- **API Development**: Analyze and optimize API responses during development
- **API Documentation**: Auto-generate documentation from live responses
- **API Testing**: Compare responses across versions for regression testing
- **API Debugging**: Quickly identify issues in API response structure
- **API Migration**: Track changes when migrating between API versions

## Built With

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [structlog](https://www.structlog.org/) - Structured logging

## Inspired By

This project was built during **DevConf Pune 2025** organized by Red Hat. The workshop on "Building Your Own MCP Server" demonstrated how MCP enables AI systems to shift from generating text to orchestrating actions.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

Apache 2.0 - See [LICENSE](LICENSE) file for details

## Author

**Shriyans** - Built during DevConf Pune 2025

## Acknowledgments

- Red Hat and DevConf Pune organizers
- FastMCP framework creators
- Model Context Protocol community

---

⭐ If you find this useful, please star the repository!

🐛 Found a bug? [Open an issue](https://github.com/YOUR_USERNAME/api-intelligence-mcp/issues)

💡 Have ideas? [Start a discussion](https://github.com/YOUR_USERNAME/api-intelligence-mcp/discussions)
