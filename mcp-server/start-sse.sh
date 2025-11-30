#!/bin/bash
# Start the MCP Weather server with SSE transport for external clients
cd "$(dirname "$0")"
uv run weather_server --transport sse
