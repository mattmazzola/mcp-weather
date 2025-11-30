# MCP Weather Server

https://modelcontextprotocol.io/docs/develop/build-server

## Getting Started

This server supports both MCP and REST API modes. See [ARCHITECTURE.md](ARCHITECTURE.md) for full details.

### Start MCP Server (STDIO Mode)

For local clients like the Python client:

```sh
uv run weather_server
# or with explicit mode:
uv run weather_server --mode mcp --transport stdio
```

### Start MCP Server (SSE Mode)

For remote clients (e.g., VS Code Copilot Chat on host machine):

```sh
uv run weather_server --mode mcp --transport sse
```

### Start REST API Server

```sh
uv run weather_server --mode api --api-port 8080
```

### Start Both MCP and REST API

```sh
uv run weather_server --mode both --mcp-port 8000 --api-port 8080
```

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture and best practices
- [DUAL_TRANSPORT.md](../DUAL_TRANSPORT.md) - Guide for devcontainer + VS Code integration
