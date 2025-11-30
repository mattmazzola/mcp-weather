#!/bin/bash
# Start the MCP Weather server with SSE transport for external clients
cd "$(dirname "$0")"
uv run python -m weather_server --transport sse
