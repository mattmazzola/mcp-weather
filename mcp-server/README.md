# MCP Server

https://modelcontextprotocol.io/docs/develop/build-server

## Getting Started

### Start in STDIO Mode

```sh
uv run weather.py
```

### Start in SSE Mode

Used to expose MCP server over HTTP for remote clients such as VS Code Copilot Chat on host machine.

```sh
uv run weather.py --transport sse
```
