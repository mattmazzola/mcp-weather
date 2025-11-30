# MCP Weather Server

A Model Context Protocol (MCP) server that exposes weather tools using FastMCP and the National Weather Service API.

## Features

This MCP server provides two main tools:

- **get_alerts**: Get weather alerts for a US state
- **get_forecast**: Get weather forecast for a location using latitude/longitude

## Prerequisites

- Python 3.12+
- [UV](https://docs.astral.sh/uv/) package manager

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

### Running the server

Run the MCP server using:

```bash
uv run python weather.py
```

Or using the script entry point:

```bash
uv run mcp-weather
```

### Configuring with Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-weather",
        "run",
        "mcp-weather"
      ]
    }
  }
}
```

Replace `/path/to/mcp-weather` with the actual path to this repository.

### Available Tools

#### get_alerts

Get weather alerts for a US state.

**Parameters:**
- `state` (string): Two-letter US state code (e.g., CA, NY, TX)

**Example:**
```
Get weather alerts for California
```

#### get_forecast

Get weather forecast for a location.

**Parameters:**
- `latitude` (float): Latitude of the location (e.g., 37.7749)
- `longitude` (float): Longitude of the location (e.g., -122.4194)

**Example:**
```
Get the weather forecast for San Francisco (37.7749, -122.4194)
```

## Development

### Dev Container

This project includes a dev container configuration for VS Code. Open the project in VS Code and use the "Reopen in Container" option to set up the development environment automatically.

### Running Tests

```bash
uv run pytest
```

## License

MIT
