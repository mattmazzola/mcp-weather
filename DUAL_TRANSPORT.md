# MCP Weather Server - Dual Transport Mode

This MCP server supports two transport modes:

## 1. STDIO Mode (Default - For Local Clients)

Use this for clients running in the same environment (e.g., your Python client):

```bash
cd mcp-server
uv run python -m weather_server
```

This is used by your existing `mcp-client/client.py` and works perfectly inside the devcontainer.

## 2. Docker Exec Mode (For VS Code on Host with Devcontainer)

VS Code's MCP integration requires spawning a stdio-based process. When your server runs in a devcontainer, use `docker exec` to bridge from the host into the container.

### Configure VS Code on Host

Add this to your **User settings** on the host machine (`~/.config/Code/User/settings.json` on Linux, `~/Library/Application Support/Code/User/settings.json` on Mac):

```json
{
  "github.copilot.chat.mcp.servers": {
    "weather": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "5d649272e1d8",
        "/bin/bash",
        "-c",
        "cd /workspaces/mcp-weather/mcp-server && /usr/local/bin/uv run python -m weather_server"
      ]
    }
  }
}
```

**Important:** Replace `5d649272e1d8` with your actual container ID or name:
- Find it by running `docker ps` on your host
- Or use the container name (e.g., `mcp-weather-devcontainer`)

### Steps

1. **Add the configuration** to your host VS Code User settings
2. **Reload VS Code** on the host
3. **Open Copilot Chat** and click "Configure Tools"
4. **Verify** the "weather" server appears in the list

You do NOT need the SSE server running for this approach - it uses stdio through docker exec.

## Summary

- **Local client (inside container)**: `uv run weather` (stdio transport) - works with your existing Python client
- **VS Code from host**: Use `docker exec` configuration above - VS Code spawns the process inside the container
- **SSE mode**: Available via `uv run weather --transport sse` for other use cases, but not needed for VS Code integration

Note: The `weather` command now runs the unified server with default MCP stdio mode. See [mcp-server/ARCHITECTURE.md](mcp-server/ARCHITECTURE.md) for the full architecture.
